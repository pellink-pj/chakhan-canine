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


st.set_page_config(
    page_title="우리 집에 맞는 강아지 찾기",
    page_icon="🐕",
    layout="wide",
)


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

        # 비용 (현재 / 시니어)
        render_cost_box(breed)

        st.markdown("")
        # 산책 · 훈련
        col1, col2 = st.columns(2)
        walk = scores.get("exercise_needs", {})
        col1.markdown(f"**🚶 산책**  \n하루 {walk.get('daily_walk_minutes','—')}분 ({walk.get('level_kr','')})")
        train = scores.get("training_difficulty", {})
        col2.markdown(f"**🎓 훈련**  \n난이도 {train.get('level_kr','—')}")

        # 상세 펼침
        with st.expander("📖 자세히 알아보기"):
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


def reset():
    st.session_state.step = "intro"
    st.session_state.answers = None
    st.session_state.appearance = None
    st.session_state.show_appearance = False
    st.session_state.picked_breed_id = None


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
                "3가지 질문에 답하시면 라이프스타일에 잘 맞는 강아지를 추천해드릴게요."
            )
            if st.button("추천 받기", use_container_width=True, type="primary", key="btn_recommend"):
                st.session_state.step = "questions"
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
# STEP 2-B / 3: 라이프스타일 질문 화면
# ════════════════════════════════════════════════════════════════

elif st.session_state.step == "questions":

    col_back, _ = st.columns([1, 5])
    if col_back.button("← 처음으로"):
        reset()
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
    results = recommend(
        breeds=breeds,
        answers=st.session_state.answers,
        appearance=st.session_state.appearance,
        top_n=12,
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
