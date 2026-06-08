"""
🐶 강아지 키우기 (Pup Hero Lab)

견종 추천 데이터를 기반으로 가상의 강아지를 키워보는 다마고치 스타일 앱.
Claude Haiku로 견종 성격에 맞는 대사 생성.

실행:
    export ANTHROPIC_API_KEY="sk-ant-..."
    streamlit run app.py
"""

import json
import time
from pathlib import Path
import streamlit as st

from tamagotchi import (
    INITIAL_STATS,
    STAT_LABELS_KR,
    apply_action,
    passive_decay,
    get_mood,
)
from claude_client import generate_reaction


st.set_page_config(
    page_title="🐶 강아지 키우기 - Pup Hero",
    page_icon="🐕",
    layout="centered",
)


# ─── 데이터 로드 ─────────────────────────────────────────

@st.cache_data
def load_breeds():
    path = Path(__file__).parent / "data" / "breeds.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["breeds"]


breeds = load_breeds()


# ─── 세션 상태 ─────────────────────────────────────────────

if "step" not in st.session_state:
    st.session_state.step = "select"  # select → playing
if "breed" not in st.session_state:
    st.session_state.breed = None
if "stats" not in st.session_state:
    st.session_state.stats = None
if "last_tick" not in st.session_state:
    st.session_state.last_tick = time.time()
if "log" not in st.session_state:
    st.session_state.log = []  # 최근 대사들 [{action, message, timestamp}]


def reset():
    for k in ["step", "breed", "stats", "last_tick", "log"]:
        if k in st.session_state:
            del st.session_state[k]


# ─── 헤더 ──────────────────────────────────────────────────

st.title("🐶 강아지 키우기")
st.caption("Pup Hero Lab — 가상으로 견종 키워보기")


# ═══════════════════════════════════════════════════════════
# STEP 1: 견종 선택
# ═══════════════════════════════════════════════════════════

if st.session_state.step == "select":
    st.markdown("### 어떤 강아지를 키워볼까요?")

    # 한국 인기 견종 우선 정렬
    popular_first = sorted(
        breeds,
        key=lambda b: (b.get("kr_popularity_rank") is None,
                       b.get("kr_popularity_rank") or 9999)
    )

    def fmt(b):
        kr = b.get("kr_name") or b["breed_name"]
        rank = b.get("kr_popularity_rank")
        return f"{kr} ({b['breed_name']})" + (f" · 한국 {rank}위" if rank and rank <= 50 else "")

    selected_label = st.selectbox(
        "견종 선택",
        options=[fmt(b) for b in popular_first],
        label_visibility="collapsed",
    )

    selected_breed = next(b for b in popular_first if fmt(b) == selected_label)

    # 선택한 견종 미리보기
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            img_url = selected_breed.get("images", {}).get("standard")
            if img_url:
                try:
                    st.image(img_url, use_container_width=True)
                except Exception:
                    st.caption("(이미지 로드 실패)")
        with col2:
            st.markdown(f"### {selected_breed.get('kr_name', selected_breed['breed_name'])}")
            temperament = selected_breed.get("temperament", [])
            if temperament:
                st.caption("성격: " + ", ".join(temperament[:5]))
            scores = selected_breed.get("scores", {})
            st.write(f"- 에너지: {scores.get('exercise_needs', {}).get('level_kr', '—')}")
            st.write(f"- 훈련: {scores.get('training_difficulty', {}).get('level_kr', '—')}")
            st.write(f"- 친화력: {scores.get('friendliness', {}).get('level_kr', '—')}")

    if st.button("🐾 이 강아지 키우기 시작!", use_container_width=True, type="primary"):
        st.session_state.breed = selected_breed
        st.session_state.stats = INITIAL_STATS.copy()
        st.session_state.last_tick = time.time()
        # 첫 인사 메시지 생성
        with st.spinner("강아지가 다가오는 중..."):
            greeting = generate_reaction(
                selected_breed, "greet", st.session_state.stats
            )
        st.session_state.log = [{"action": "greet", "message": greeting}]
        st.session_state.step = "playing"
        st.rerun()


# ═══════════════════════════════════════════════════════════
# STEP 2: 다마고치 메인 화면
# ═══════════════════════════════════════════════════════════

elif st.session_state.step == "playing":

    breed = st.session_state.breed
    stats = st.session_state.stats

    # ── Passive decay (마지막 액션 후 흐른 시간만큼 자연 변화) ──
    now = time.time()
    elapsed_min = (now - st.session_state.last_tick) / 60
    if elapsed_min >= 1:
        stats = passive_decay(stats, elapsed_min, breed)
        st.session_state.stats = stats
        st.session_state.last_tick = now

    # ── 상단 견종 정보 + 처음으로 ──
    col_back, col_info, _ = st.columns([1, 4, 1])
    if col_back.button("🔄"):
        reset()
        st.rerun()
    col_info.markdown(
        f"### {breed.get('kr_name', breed['breed_name'])} "
        f"<small style='color:gray'>({breed['breed_name']})</small>",
        unsafe_allow_html=True,
    )

    # ── 강아지 메인 화면 (이모지 + 기분) ──
    mood_emoji, mood_text = get_mood(stats)
    with st.container(border=True):
        st.markdown(
            f"<div style='text-align:center; padding: 30px 10px;'>"
            f"<div style='font-size:96px; line-height:1;'>{mood_emoji}</div>"
            f"<div style='font-size:18px; margin-top:12px; color:#555;'>{mood_text}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── 스탯 표시 ────────────────────────────────────────
    st.markdown("##### 강아지 상태")
    for stat_key, value in stats.items():
        label, emoji = STAT_LABELS_KR[stat_key]
        value_int = int(value)
        # 배고픔은 낮을수록 좋음 — 표시는 100-value로 변환해서 직관적으로
        if stat_key == "hunger":
            display_value = 100 - value_int
            display_label = "배부름"
            display_emoji = "🍖"
        else:
            display_value = value_int
            display_label = label
            display_emoji = emoji

        col_l, col_r = st.columns([1, 4])
        col_l.markdown(f"{display_emoji} **{display_label}**")
        col_r.progress(display_value / 100, text=f"{display_value}/100")

    # ── 인터랙션 버튼 ──────────────────────────────────
    st.markdown("##### 강아지와 시간 보내기")
    col1, col2, col3, col4 = st.columns(4)

    def do_action(action_name: str, button_label: str):
        with st.spinner(f"{button_label} 중..."):
            new_stats = apply_action(stats, action_name, breed)
            st.session_state.stats = new_stats
            message = generate_reaction(breed, action_name, new_stats)
        st.session_state.log.insert(0, {"action": action_name, "message": message})
        # 로그는 최근 8개만 유지
        st.session_state.log = st.session_state.log[:8]
        st.session_state.last_tick = time.time()
        st.rerun()

    if col1.button("🍖\n먹이 주기", use_container_width=True):
        do_action("feed", "밥 주기")
    if col2.button("🚶\n산책 가기", use_container_width=True):
        do_action("walk", "산책")
    if col3.button("🎓\n훈련 시키기", use_container_width=True):
        do_action("train", "훈련")
    if col4.button("🎾\n같이 놀기", use_container_width=True):
        do_action("play", "놀이")

    # ── 강아지 대사 로그 ───────────────────────────────
    if st.session_state.log:
        st.markdown("##### 💬 강아지의 한마디")
        for i, entry in enumerate(st.session_state.log):
            opacity = 1.0 if i == 0 else 0.6
            with st.container(border=True):
                st.markdown(
                    f"<div style='opacity:{opacity};'>"
                    f"<small style='color:gray;'>"
                    f"{ {'feed':'🍖 먹이', 'walk':'🚶 산책', 'train':'🎓 훈련', 'play':'🎾 놀이', 'greet':'👋 인사'}.get(entry['action'], '') }"
                    f"</small><br>{entry['message']}</div>",
                    unsafe_allow_html=True,
                )
