"""
견종 추천 프로토타입 (Streamlit)

실행:
    pip install streamlit
    streamlit run app.py

흐름:
  [intro] 시작 화면 — "마음에 둔 강아지가 있으세요?"
     ├─ "있어요" → [breed_picked] 견종 선택 → 특징 표시 → "라이프스타일 매칭?" 옵션
     │      └─ 선택 시 → [questions] 3개 질문 → [results] 매칭 결과
     │
     └─ "추천 받고 싶어요" → [questions] 3개 질문 → [results] 매칭 결과
"""

import streamlit as st
from pathlib import Path

from recommender import (
    recommend,
    load_breeds,
    compute_match_score,
    BUDGET_OPTIONS,
    WALK_OPTIONS,
    TRAINING_OPTIONS,
    SIZE_OPTIONS,
    COAT_LENGTH_OPTIONS,
)
from journey import (
    QUESTIONS,
    STAGES,
    SHOCK_CARDS,
    questions_by_stage,
    collect_insights,
    get_recommendation_modifiers,
    get_opening_message,
)
from breed_messages import (
    get_trait_messages,
    get_founder_message_if_relevant,
)


st.set_page_config(
    page_title="우리 집에 맞는 강아지 찾기",
    page_icon="🐕",
    layout="wide",
)


# ─── 폰트 + 테마 (따뜻한 톤) ───────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/webfontworld/nanum/NanumSquareRound.css');

/* 전체 앱에 나눔스퀘어 라운드 적용 */
html, body, [class*="css"], [class*="st-"], button, input, textarea, select {
    font-family: 'NanumSquareRound', 'Apple SD Gothic Neo', sans-serif !important;
}

/* 타이틀·헤더는 굵게 */
h1, h2, h3, h4 {
    font-family: 'NanumSquareRound', 'Apple SD Gothic Neo', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

/* 따뜻한 색감 — 멍메이트 팔레트 */
:root {
    --coral: #E8574A;
    --orange: #F08040;
    --yellow: #F5C842;
    --soft-bg: #FFF8F2;
}

/* primary 버튼: 코랄→오렌지 그라데이션 */
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #E8574A, #F08040) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(232,87,74,0.25);
}
.stButton button[kind="primary"]:hover {
    box-shadow: 0 6px 18px rgba(232,87,74,0.35);
    transform: translateY(-1px);
    transition: all 0.15s ease;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_breeds():
    return load_breeds(Path(__file__).parent / "processed" / "breeds.json")


# ════════════════════════════════════════════════════════════════
# 공용 컴포넌트
# ════════════════════════════════════════════════════════════════

def render_cost_box(breed: dict):
    """현재 비용 + 시니어 비용 박스 (카드/특징 페이지 공용)"""
    c = breed.get("cost_estimate", {})
    cur = c.get("current", {})
    sen = c.get("senior", {})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**💰 현재 (어린 시기)**")
        st.markdown(
            f"월 {cur.get('monthly_krw_min',0)//10000}~{cur.get('monthly_krw_max',0)//10000}만원 "
            f"<span style='color:gray'>({cur.get('level_kr','—')})</span>",
            unsafe_allow_html=True,
        )
        st.caption("사료·그루밍·용품·기본 의료비")
    with col2:
        st.markdown("**🏥 시니어 (7세+)**")
        st.markdown(
            f"월 {sen.get('monthly_krw_min',0)//10000}~{sen.get('monthly_krw_max',0)//10000}만원 "
            f"<span style='color:gray'>({sen.get('level_kr','—')})</span>",
            unsafe_allow_html=True,
        )
        risks = sen.get("risk_factors", [])
        if risks:
            st.caption("⚠ " + " · ".join(risks))
        else:
            st.caption("정기 검진·관절 관리 일반 수준")


def render_breed_card(breed: dict, show_match: bool = True):
    """견종 카드 1장. show_match=False면 매칭도 숨김(견종 미리 정한 경우)"""
    name_kr = breed.get("kr_name") or breed["breed_name"]
    name_en = breed["breed_name"]
    scores = breed.get("scores", {})

    with st.container(border=True):
        img_url = breed.get("images", {}).get("standard")
        if img_url:
            try:
                st.image(img_url, use_container_width=True)
            except Exception:
                st.caption("(이미지 로드 실패)")

        col_name, col_match = st.columns([2, 1])
        col_name.markdown(f"### {name_kr}")
        col_name.caption(name_en)
        if show_match and "_match" in breed:
            col_match.metric("매칭", f"{breed['_match']['percent']}%")

        kr_rank = breed.get("kr_popularity_rank")
        if kr_rank and kr_rank <= 10:
            st.markdown(f"🥇 **한국 인기 {kr_rank}위**")
        elif kr_rank:
            st.caption(f"🇰🇷 한국 인기 {kr_rank}위")

        # 시야 확장 추천 뱃지
        if breed.get("_horizon_pick"):
            st.markdown(
                "🌍 **시야를 넓혀볼 견종**  \n"
                "<small style='color:gray'>한국에선 흔치 않지만 당신과 잘 맞을 수 있어요</small>",
                unsafe_allow_html=True,
            )

        # 비용 (현재 / 시니어)
        render_cost_box(breed)

        st.markdown("")
        # 산책 · 훈련
        col1, col2 = st.columns(2)
        walk = scores.get("exercise_needs", {})
        col1.markdown(f"**🚶 산책**  \n하루 {walk.get('daily_walk_minutes','—')}분 ({walk.get('level_kr','')})")
        train = scores.get("training_difficulty", {})
        col2.markdown(f"**🎓 훈련**  \n난이도 {train.get('level_kr','—')}")

        # ─── 멍메이트 톤 메시지 (훈련 희망) ────────────────
        trait_msgs = get_trait_messages(breed)
        if trait_msgs:
            st.markdown("")
            for m in trait_msgs[:3]:   # 카드에선 최대 3개만 (상세에서 전부)
                bg_color = {
                    "good":    "#F0F9F0",   # 연한 초록
                    "hope":    "#FFF8E8",   # 연한 노랑
                    "caution": "#FFF0EC",   # 연한 코랄
                }.get(m["tone"], "#F8F8F8")
                border_color = {
                    "good":    "#86C86A",
                    "hope":    "#F0A040",
                    "caution": "#E8574A",
                }.get(m["tone"], "#CCC")
                st.markdown(
                    f"""<div style='
                        background: {bg_color};
                        border-left: 3px solid {border_color};
                        border-radius: 6px;
                        padding: 10px 12px;
                        margin: 4px 0;
                        font-size: 13.5px;
                        line-height: 1.5;
                    '>
                        <span style='
                            display: inline-block;
                            font-size: 11px;
                            color: #888;
                            background: rgba(0,0,0,0.04);
                            padding: 1px 8px;
                            border-radius: 4px;
                            margin-bottom: 4px;
                        '>{m['category']}</span>
                        <div><b>{m['title']}</b></div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        # 창업자 셸티 사례 (관련 견종에만)
        founder_msg = get_founder_message_if_relevant(breed)
        if founder_msg:
            st.markdown(
                f"""<div style='
                    background: linear-gradient(135deg, #FFF8F2, #FFF);
                    border: 1px dashed #E8574A88;
                    border-radius: 8px;
                    padding: 10px 14px;
                    margin: 8px 0;
                    font-size: 13px;
                    color: #5A4030;
                    line-height: 1.6;
                '>
                    {founder_msg}
                </div>""",
                unsafe_allow_html=True,
            )

        # 상세 펼침
        with st.expander("📖 자세히 알아보기"):
            # 상세에선 모든 trait 메시지 + 텍스트도 보여줌
            if trait_msgs:
                st.markdown("**🎯 이 견종과 함께 살려면**")
                for m in trait_msgs:
                    st.markdown(f"- `{m['category']}` **{m['title']}**")
                    st.caption(m["text"])
                st.markdown("---")
            chunks = breed.get("rag_chunks", [])
            for ch in chunks:
                st.markdown(f"**{ch['topic_kr']}**")
                st.write(ch["text"])

            st.markdown("---")
            st.markdown("**견종 기본 정보**")
            info_col1, info_col2 = st.columns(2)
            info_col1.write(f"📏 체중: {breed.get('weight_kr', '—')}")
            info_col1.write(f"📐 키: {breed.get('height_kr', '—')}")
            info_col2.write(f"❤️ 수명: {breed.get('life_expectancy', '—')}")
            info_col2.write(f"🏷️ 크기: {breed.get('size_category_kr', '—')}")

            tags = breed.get("lifestyle_tags", [])
            if tags:
                st.markdown("**특징**: " + " ".join(f"`{t}`" for t in tags))


# ════════════════════════════════════════════════════════════════
# 세션 상태
# ════════════════════════════════════════════════════════════════

if "step" not in st.session_state:
    st.session_state.step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = None
if "appearance" not in st.session_state:
    st.session_state.appearance = None
if "show_appearance" not in st.session_state:
    st.session_state.show_appearance = False
if "picked_breed_id" not in st.session_state:
    st.session_state.picked_breed_id = None
if "journey_answers" not in st.session_state:
    st.session_state.journey_answers = {}   # Q_id → 답변값
if "shock_index" not in st.session_state:
    st.session_state.shock_index = 0        # 충격 카드 페이지 인덱스


def reset():
    st.session_state.step = "intro"
    st.session_state.answers = None
    st.session_state.appearance = None
    st.session_state.show_appearance = False
    st.session_state.picked_breed_id = None
    st.session_state.journey_answers = {}
    st.session_state.shock_index = 0


def render_journey_stage(stage_key: str, stage_emoji: str, stage_name: str, next_step: str, prev_step: str, stage_index: int, total_stages: int):
    """3단계 여정 페이지 1개 렌더링. 다음/이전 페이지 자동 처리."""
    questions = questions_by_stage(stage_key)

    # 진행률 표시
    progress_value = stage_index / total_stages
    st.progress(progress_value, text=f"입양 준비 여정 — {stage_emoji} {stage_name} ({stage_index}/{total_stages})")
    st.caption(
        "추천 전에 함께 생각해볼 것들이에요. "
        "솔직하게 답해주시면 더 잘 맞는 견종을 찾아드릴 수 있어요."
    )
    st.markdown("")

    with st.form(f"journey_{stage_key}"):
        for q in questions:
            st.subheader(q["question"])
            if q.get("helper"):
                st.caption(q["helper"])

            current = st.session_state.journey_answers.get(q["id"])
            option_labels = [opt["label"] for opt in q["options"]]
            default_index = 0
            if current:
                for i, opt in enumerate(q["options"]):
                    if opt["value"] == current:
                        default_index = i
                        break

            selected_label = st.radio(
                q["id"],
                options=option_labels,
                index=default_index,
                label_visibility="collapsed",
                key=f"radio_{q['id']}",
            )
            # 임시 저장 (제출 전이라도 기억)
            for opt in q["options"]:
                if opt["label"] == selected_label:
                    st.session_state.journey_answers[q["id"]] = opt["value"]
                    break

            st.divider()

        col_prev, col_next = st.columns([1, 2])
        prev = col_prev.form_submit_button("← 이전", use_container_width=True)
        nxt = col_next.form_submit_button("다음 →", use_container_width=True, type="primary")

        if prev:
            st.session_state.step = prev_step
            st.rerun()
        if nxt:
            st.session_state.step = next_step
            st.rerun()


# ════════════════════════════════════════════════════════════════
# 헤더 & 데이터
# ════════════════════════════════════════════════════════════════

st.title("🐕 우리 집에 맞는 강아지 찾기")

breeds = get_breeds()


# ════════════════════════════════════════════════════════════════
# STEP 1: 시작 화면 — 견종 미리 정했는지 분기
# ════════════════════════════════════════════════════════════════

if st.session_state.step == "intro":
    st.caption("입양을 고민 중이신가요? 라이프스타일에 맞는 강아지를 찾아드릴게요.")

    st.markdown("")
    st.subheader("마음에 둔 강아지가 있으세요?")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 🐶 네, 키우고 싶은 견종이 있어요")
            st.caption(
                "이미 마음에 둔 견종의 특징을 보고, "
                "내 라이프스타일에 정말 맞는지 함께 알아봐요."
            )
            if st.button("견종 선택하기", use_container_width=True, type="primary", key="btn_pick"):
                st.session_state.step = "breed_picked"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### 🤔 아직 잘 모르겠어요")
            st.caption(
                "함께 천천히 알아봐요. 입양 전에 알아두면 좋을 것들과 "
                "라이프스타일에 잘 맞는 강아지를 함께 보여드릴게요."
            )
            if st.button("함께 알아보기", use_container_width=True, type="primary", key="btn_recommend"):
                st.session_state.step = "journey_shock"
                st.session_state.shock_index = 0
                st.rerun()


# ════════════════════════════════════════════════════════════════
# STEP 2-A: 견종 선택 — 특징 보여주고 라이프스타일 매칭 옵션
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "breed_picked":

    # 한국 인기 견종을 위로 정렬한 옵션 리스트
    popular_first = sorted(
        breeds,
        key=lambda b: (b.get("kr_popularity_rank") is None,
                       b.get("kr_popularity_rank") or 9999)
    )

    def fmt_breed(b):
        kr = b.get("kr_name") or b["breed_name"]
        rank = b.get("kr_popularity_rank")
        if rank and rank <= 50:
            return f"{kr} ({b['breed_name']}) · 한국 {rank}위"
        return f"{kr} ({b['breed_name']})"

    col_back, _ = st.columns([1, 5])
    if col_back.button("← 돌아가기"):
        reset()
        st.rerun()

    st.subheader("어떤 강아지가 마음에 두셨어요?")

    selected_label = st.selectbox(
        "견종을 선택하세요",
        options=[fmt_breed(b) for b in popular_first],
        index=0 if not st.session_state.picked_breed_id else
              next((i for i, b in enumerate(popular_first)
                    if b["_id"] == st.session_state.picked_breed_id), 0),
        placeholder="견종 이름 입력하거나 선택",
    )

    selected_breed = next(
        b for b in popular_first if fmt_breed(b) == selected_label
    )
    st.session_state.picked_breed_id = selected_breed["_id"]

    st.divider()

    # 선택한 견종 특징 카드
    st.markdown(f"### 🐾 {selected_breed.get('kr_name', selected_breed['breed_name'])}의 특징")
    render_breed_card(selected_breed, show_match=False)

    st.divider()

    # 라이프스타일 매칭 옵션
    with st.container(border=True):
        st.markdown("#### 🔍 내 라이프스타일에 맞는지 알아볼까요?")
        st.caption(
            "이 견종이 정말 우리 집에 잘 맞을지 3가지 질문으로 확인해드릴게요. "
            "비슷한 성격·관리법을 가진 다른 견종도 함께 추천돼요."
        )
        if st.button("✨ 라이프스타일 매칭하기", use_container_width=True, type="primary"):
            st.session_state.step = "questions"
            st.rerun()


# ════════════════════════════════════════════════════════════════
# Stage 0 — 인지 충격 카드 (한국 통계 기반)
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "journey_shock":
    idx = st.session_state.shock_index
    total = len(SHOCK_CARDS)
    card = SHOCK_CARDS[idx]

    # 진행 표시
    st.progress((idx + 1) / (total + 4), text=f"잠시 함께 알아봐요 ({idx+1}/{total})")

    # 카드 본체
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #FFF8F2, #fff);
        border: 2px solid #E8574A22;
        border-radius: 24px;
        padding: 48px 36px;
        margin: 16px 0;
        text-align: center;
        min-height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    '>
        <div style='font-size: 64px; line-height: 1; margin-bottom: 12px;'>{card["icon"]}</div>
        <div style='font-size: 18px; color: #666; font-weight: 600;'>{card["headline"]}</div>
        <div style='font-size: 64px; font-weight: 900; color: #E8574A; letter-spacing: -0.03em; margin: 8px 0;'>
            {card["big_stat"]}
        </div>
        <div style='font-size: 18px; color: #444; font-weight: 700; margin-bottom: 28px;'>{card["stat_label"]}</div>
        <div style='font-size: 15px; color: #555; line-height: 1.8; max-width: 540px; margin: 0 auto; text-align: left; font-weight: 500;'>
            {card["subtext"].replace(chr(10), "<br>").replace("**", "<b>", 1).replace("**", "</b>", 1).replace("**", "<b>", 1).replace("**", "</b>", 1).replace("**", "<b>", 1).replace("**", "</b>", 1)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 네비게이션
    col_back, col_skip, col_next = st.columns([1, 1, 2])
    if col_back.button("← 이전", disabled=(idx == 0), use_container_width=True):
        st.session_state.shock_index -= 1
        st.rerun()
    if col_skip.button("건너뛰기", use_container_width=True):
        st.session_state.step = "journey_myth"
        st.rerun()
    if col_next.button(card["next_label"], use_container_width=True, type="primary"):
        if idx + 1 < total:
            st.session_state.shock_index += 1
            st.rerun()
        else:
            # 마지막 카드 → 자가진단으로
            st.session_state.step = "journey_myth"
            st.rerun()


# ════════════════════════════════════════════════════════════════
# 3단계 여정 — Stage 1 (오해 깨기)
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "journey_myth":
    render_journey_stage(
        stage_key="myth", stage_emoji="🟨", stage_name="흔한 오해 깨기",
        prev_step="intro", next_step="journey_horizon",
        stage_index=1, total_stages=4,
    )

# ════════════════════════════════════════════════════════════════
# 3단계 여정 — Stage 2 (시야 확장)
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "journey_horizon":
    render_journey_stage(
        stage_key="horizon", stage_emoji="🟩", stage_name="시야 확장",
        prev_step="journey_myth", next_step="journey_reality",
        stage_index=2, total_stages=4,
    )

# ════════════════════════════════════════════════════════════════
# 3단계 여정 — Stage 3 (현실 인식)
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "journey_reality":
    render_journey_stage(
        stage_key="reality", stage_emoji="🟥", stage_name="현실 인식",
        prev_step="journey_horizon", next_step="questions",
        stage_index=3, total_stages=4,
    )


# ════════════════════════════════════════════════════════════════
# STEP 2-B / 3: 라이프스타일 질문 화면
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "questions":

    # 여정에서 들어왔으면 progress bar 표시
    if st.session_state.journey_answers:
        st.progress(4 / 4, text="입양 준비 여정 — 🟦 라이프스타일 매칭 (4/4)")
        st.caption("마지막이에요. 당신의 일상에 맞을 견종을 매칭해드릴게요.")
        st.markdown("")

    col_back, _ = st.columns([1, 5])
    back_target = "journey_reality" if st.session_state.journey_answers else "intro"
    if col_back.button("← 이전"):
        st.session_state.step = back_target
        st.rerun()

    # 선택한 견종이 있으면 상단에 안내
    if st.session_state.picked_breed_id:
        picked = next(
            (b for b in breeds if b["_id"] == st.session_state.picked_breed_id), None
        )
        if picked:
            st.info(
                f"마음에 둔 견종: **{picked.get('kr_name', picked['breed_name'])}** "
                f"— 답변하시면 매칭도와 함께 비슷한 견종도 보여드릴게요"
            )

    with st.form("questions_form"):
        st.subheader("Q1. 강아지 한 달 양육비, 어느 정도까지 가능하세요?")
        st.caption("사료·그루밍·기본 의료비·용품을 합한 입양 초반 월 비용입니다 (시니어 의료비는 별도)")
        budget_label = st.radio(
            "예산",
            options=[o["label"] for o in BUDGET_OPTIONS],
            index=1,
            label_visibility="collapsed",
        )

        st.divider()

        st.subheader("Q2. 하루에 얼마나 산책시킬 수 있으세요?")
        st.caption("강아지마다 필요한 운동량이 크게 달라요")
        walk_label = st.radio(
            "산책",
            options=[o["label"] for o in WALK_OPTIONS],
            index=1,
            label_visibility="collapsed",
        )

        st.divider()

        st.subheader("Q3. 훈련에 시간을 들일 수 있으세요?")
        st.markdown(
            "💡 *훈련을 잘 시키면 강아지가 자신감과 안정감을 얻어 짖음·분리불안 같은 "
            "문제 행동이 크게 줄어들어요. 보호자와의 신뢰 관계도 깊어지고 가족 전체가 행복해집니다.*"
        )
        training_label = st.radio(
            "훈련",
            options=[o["label"] for o in TRAINING_OPTIONS],
            index=1,
            label_visibility="collapsed",
        )

        st.divider()
        submit = st.form_submit_button(
            "✨ 결과 보기",
            use_container_width=True,
            type="primary",
        )

        if submit:
            budget = next(o for o in BUDGET_OPTIONS if o["label"] == budget_label)
            walk = next(o for o in WALK_OPTIONS if o["label"] == walk_label)
            training = next(o for o in TRAINING_OPTIONS if o["label"] == training_label)

            st.session_state.answers = {
                "budget_level": budget["level"],
                "walk_minutes": walk["minutes"],
                "willingness": training["willingness"],
            }
            st.session_state.step = "results"
            st.rerun()


# ════════════════════════════════════════════════════════════════
# STEP 3: 결과 화면
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "results":

    a = st.session_state.answers
    budget_label = next(o["label"] for o in BUDGET_OPTIONS if o["level"] == a["budget_level"])
    walk_label = next(o["label"] for o in WALK_OPTIONS if o["minutes"] == a["walk_minutes"])
    train_label = next(o["label"] for o in TRAINING_OPTIONS if o["willingness"] == a["willingness"])

    # 답변 요약
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
        col1.markdown(f"**💰 예산**\n\n{budget_label}")
        col2.markdown(f"**🚶 산책**\n\n{walk_label}")
        col3.markdown(f"**🎓 훈련**\n\n{train_label.split('(')[0].strip()}")
        if col4.button("🔄 처음부터", use_container_width=True):
            reset()
            st.rerun()

    # ── 여정 답변이 있으면: 인사이트 메시지 카드 표시 ──
    if st.session_state.journey_answers:
        insights = collect_insights(st.session_state.journey_answers)
        opening = get_opening_message(st.session_state.journey_answers)

        st.markdown("")
        with st.container(border=True):
            st.markdown(f"### 💌 당신의 마음을 들었어요")
            st.write(opening)

            if insights:
                st.markdown("---")
                st.markdown("#### 알아두시면 좋아요")
                for ins in insights:
                    with st.container(border=True):
                        st.markdown(f"**{ins['tone']}**  \n_<small style='color:gray'>{ins['stage_kr']}</small>_", unsafe_allow_html=True)
                        st.markdown(ins["text"])
        st.markdown("")

    # ── 마음에 둔 견종이 있으면: 그 견종 매칭도 결과 먼저 보여줌 ──
    if st.session_state.picked_breed_id:
        picked = next(
            (b for b in breeds if b["_id"] == st.session_state.picked_breed_id), None
        )
        if picked:
            match = compute_match_score(picked, st.session_state.answers)
            picked_with_match = {**picked, "_match": match}

            st.markdown("### 🎯 마음에 둔 견종과의 매칭")
            col_l, col_r = st.columns([1, 2])
            with col_l:
                render_breed_card(picked_with_match)
            with col_r:
                pct = match["percent"]
                if pct >= 80:
                    st.success(f"### 🎉 잘 맞아요! ({pct}% 매칭)")
                    st.markdown("라이프스타일과 잘 맞는 견종이에요. 안심하고 입양 준비를 시작하셔도 좋아요.")
                elif pct >= 60:
                    st.warning(f"### 😊 괜찮은 편 ({pct}% 매칭)")
                    st.markdown("대체로 맞지만 몇 가지 부분은 신경 써서 준비하면 좋아요.")
                else:
                    st.error(f"### ⚠️ 신중히 생각해보세요 ({pct}% 매칭)")
                    st.markdown(
                        "현재 라이프스타일과 잘 맞지 않을 수 있어요. "
                        "아래에 더 잘 맞는 견종도 함께 추천해드릴게요."
                    )

                # 항목별 점수
                bd = match["breakdown"]
                st.markdown("**항목별 매칭**")
                st.markdown(f"- 💰 예산: {bd['budget']}/30")
                st.markdown(f"- 🚶 산책: {bd['walk']}/30")
                st.markdown(f"- 🎓 훈련: {bd['training']}/30")
                st.markdown(f"- 🥇 인기 보너스: {bd['popularity_bonus']}/10")

            st.divider()
            st.markdown("### 🐾 비슷하면서 라이프스타일에 잘 맞는 다른 강아지")
        else:
            st.markdown("### 🐾 당신과 잘 맞을 것 같은 강아지")
    else:
        st.markdown("### 🐾 당신과 잘 맞을 것 같은 강아지")

    # ── 외모 필터 (펼침 상태) ──
    if st.session_state.show_appearance:
        with st.container(border=True):
            st.subheader("✨ 외모 조건 추가")
            col1, col2 = st.columns(2)
            with col1:
                size_label = st.radio(
                    "어떤 크기가 좋으세요?",
                    options=[o["label"] for o in SIZE_OPTIONS],
                )
            with col2:
                coat_label = st.radio(
                    "털 길이는 어떤 게 좋으세요?",
                    options=[o["label"] for o in COAT_LENGTH_OPTIONS],
                )

            size_val = next(o["value"] for o in SIZE_OPTIONS if o["label"] == size_label)
            coat_val = next(o["value"] for o in COAT_LENGTH_OPTIONS if o["label"] == coat_label)
            st.session_state.appearance = {"size": size_val, "coat_length": coat_val}

            if st.button("외모 조건 해제"):
                st.session_state.show_appearance = False
                st.session_state.appearance = None
                st.rerun()

    # 추천 견종 그리드
    # 여정 답변 기반 알고리즘 가중치
    journey_modifiers = get_recommendation_modifiers(st.session_state.journey_answers) \
        if st.session_state.journey_answers else {}

    results = recommend(
        breeds=breeds,
        answers=st.session_state.answers,
        appearance=st.session_state.appearance,
        top_n=12,
        journey_modifiers=journey_modifiers,
    )
    # 마음에 둔 견종은 이미 위에 보여줬으니 그리드에서 제외
    if st.session_state.picked_breed_id:
        results = [r for r in results if r["_id"] != st.session_state.picked_breed_id]

    if not results:
        st.warning("조건에 맞는 견종이 너무 적어요. 외모 조건을 풀어보세요.")
    else:
        for row_start in range(0, len(results), 3):
            row = results[row_start:row_start+3]
            cols = st.columns(3)
            for col, breed in zip(cols, row):
                with col:
                    render_breed_card(breed)

    # 외모 폴백
    st.divider()
    if not st.session_state.show_appearance:
        st.markdown("##### 🤔 추천된 강아지가 마음에 안 드세요?")
        if st.button(
            "✨ 다른 스타일도 보고 싶어요 (크기·털 길이 조건 추가)",
            use_container_width=True,
        ):
            st.session_state.show_appearance = True
            st.rerun()
