"""
입양 준비 여정 (Journey) — 멍메이트 핵심 흐름

"잘 모르겠어요" 분기로 들어온 사용자에게 보여주는 흐름.

핵심 인사이트:
  한국인은 인기·외모에 끌려 안일하게 입양 → 라이프스타일 불일치 → 유기.
  이 사이클을 끊는 것이 멍메이트의 사명.

흐름:
  Stage 0: 인지 충격 카드 ⭐ (한국 데이터로 시작)
  Stage 1: 흔한 오해 깨기 (3개)
  Stage 2: 시야 확장 (2개)
  Stage 3: 현실 인식 (3개)
  Stage 4: 라이프스타일 매칭 (3개, 기존 recommender.py 활용)
"""

from __future__ import annotations
from typing import TypedDict


# ═══════════════════════════════════════════════════════════════
# Stage 0: 인지 충격 카드 — 한국 시장 통계 기반
# ═══════════════════════════════════════════════════════════════
# 매칭 전에 사용자의 "당연한 인식"을 흔드는 단계.
# 한국 인기 TOP 10 데이터로 출처가 명확한 충격적 진실을 전달.

SHOCK_CARDS = [
    {
        "id": "shock_yougi",
        "icon": "💔",
        "headline": "한국에서 매년",
        "big_stat": "11만 마리",
        "stat_label": "강아지가 유기됩니다",
        "subtext": (
            "유기의 가장 큰 원인은 **문제 행동**과 **환경 변화**예요.\n\n"
            "그리고 가장 많이 유기되는 견종은…\n"
            "**한국에서 가장 인기 있는 견종들**과 거의 일치합니다."
        ),
        "next_label": "그게 무슨 뜻이에요?",
        "tone": "serious",
    },
    {
        "id": "shock_barking",
        "icon": "🔊",
        "headline": "한국 인기 TOP 10 중",
        "big_stat": "8마리",
        "stat_label": "가 '많이 짖는' 견종입니다",
        "subtext": (
            "푸들·포메라니안·시츄·치와와·요크셔·비숑…\n"
            "당신이 떠올린 그 귀여운 강아지, 대부분 짖음이 많아요.\n\n"
            "**공동주택이 많은 한국**에서 짖음은 이웃 갈등의 1순위.\n"
            "그리고 짖음 훈련 못 시키면 유기로 이어집니다."
        ),
        "next_label": "그럼 어떻게 해야 해요?",
        "tone": "informative",
    },
    {
        "id": "shock_patella",
        "icon": "🦴",
        "headline": "인기 TOP 10 중",
        "big_stat": "7마리",
        "stat_label": "가 슬개골 탈구 위험",
        "subtext": (
            "**작고 귀여워서 키우기 쉬울 거**라 생각하셨나요?\n\n"
            "사실 소형견은 평생 슬개골 관리가 필요하고,\n"
            "수술 시 **수백만 원**의 의료비가 들 수 있어요.\n\n"
            "강아지의 **마지막 5년**이 평생 의료비의 70%."
        ),
        "next_label": "그건 몰랐어요...",
        "tone": "informative",
    },
    {
        "id": "shock_appearance",
        "icon": "📷",
        "headline": "한국인 강아지 선택의 진실",
        "big_stat": "외모 위주",
        "stat_label": "SNS·펫샵 진열장으로 결정",
        "subtext": (
            "한국에서는 강아지를 **귀여움**으로 고르는 경우가 많아요.\n"
            "하지만 라이프스타일과 안 맞으면…\n\n"
            "→ 짖음에 지쳐서 후회\n"
            "→ 의료비 부담에 후회\n"
            "→ 결국 유기소로\n\n"
            "이건 강아지만의 문제가 아니에요.\n"
            "**우리 모두 같은 선택만 하고 있다는** 신호이기도 해요."
        ),
        "next_label": "그럼 어떻게 달라야 해요?",
        "tone": "informative",
    },
    {
        "id": "shock_signature",
        "icon": "💎",
        "headline": "한국인이 다 똑같은 견종 키울 때",
        "big_stat": "당신만의",
        "stat_label": "시그니처 견종을 찾아드릴게요",
        "subtext": (
            "**검증된 좋은 선택**이면서도\n"
            "**남들과는 다른 특별한 당신답게**.\n\n"
            "해외에선 이미 인기지만 한국에선 아직 잘 알려지지 않은\n"
            "**히든 젬 견종**들을 안목 있게 큐레이션해드려요.\n\n"
            "✨ 짖음이 적고\n"
            "✨ 의료비 부담 적고\n"
            "✨ 라이프스타일에 잘 맞으면서도\n"
            "✨ 남들과는 다른\n\n"
            "그런 강아지가 있어요."
        ),
        "next_label": "나만의 시그니처 찾기 →",
        "tone": "hopeful",
    },
]


# ═══════════════════════════════════════════════════════════════
# 기존 질문 정의
# ═══════════════════════════════════════════════════════════════



class Option(TypedDict):
    value: str
    label: str


class Question(TypedDict, total=False):
    id: str
    stage: str          # "myth" | "horizon" | "reality"
    stage_kr: str
    question: str
    helper: str         # 질문 하단 보조 설명
    options: list[Option]
    insights: dict      # answer_value → {"tone": str, "text": str}


# ─── 11개 질문 정의 ───────────────────────────────────────

QUESTIONS: list[Question] = [
    # ═══════════════ Stage 1: 흔한 오해 깨기 ═══════════════
    {
        "id": "Q1_small_easy",
        "stage": "myth",
        "stage_kr": "흔한 오해 깨기",
        "question": "작은 강아지가 큰 강아지보다 키우기 쉬울 거라 생각하시나요?",
        "options": [
            {"value": "yes",     "label": "네, 작은 게 편할 것 같아요"},
            {"value": "no",      "label": "비슷할 것 같아요"},
            {"value": "unknown", "label": "잘 모르겠어요"},
        ],
        "insights": {
            "yes": {
                "tone": "💡 사실은요",
                "text": (
                    "소형견(말티즈·푸들·치와와)은 **슬개골 탈구**가 흔하고, "
                    "예민해서 더 자주 짖는 경우도 많아요. "
                    "작은 몸집이라 쉬워 보이지만, 평생 의료비는 오히려 더 들 수 있답니다."
                ),
            },
        },
    },
    {
        "id": "Q2_monthly_cost",
        "stage": "myth",
        "stage_kr": "흔한 오해 깨기",
        "question": "한 달 양육비, 어느 정도면 충분하다고 생각하세요?",
        "options": [
            {"value": "10",      "label": "월 10만원 정도"},
            {"value": "20_30",   "label": "월 20~30만원"},
            {"value": "50_plus", "label": "월 50만원 이상도 가능"},
            {"value": "unknown", "label": "잘 모르겠어요"},
        ],
        "insights": {
            "10": {
                "tone": "💡 현실은요",
                "text": (
                    "사료·간식만 월 10만원이고, 미용·예방접종·구충제·용품을 더하면 "
                    "**최소 월 20만원**부터 시작해요. "
                    "강아지가 7세를 넘으면 정기 의료비로 **월 30~50만원**도 흔합니다."
                ),
            },
            "unknown": {
                "tone": "📊 참고로요",
                "text": (
                    "보통 어린 시기 월 20~30만원, 시니어가 되면 월 30~50만원이 평균이에요. "
                    "견종별로 차이가 커서, 결과 화면에서 견종별 비용을 자세히 보여드릴게요."
                ),
            },
        },
    },
    {
        "id": "Q3_only_owner",
        "stage": "myth",
        "stage_kr": "흔한 오해 깨기",
        "question": "강아지는 주인 한 명만 따른다고 생각하시나요?",
        "options": [
            {"value": "yes",     "label": "네, 그래서 안심돼요"},
            {"value": "no",      "label": "아니요, 사회화가 필요해요"},
            {"value": "unknown", "label": "잘 모르겠어요"},
        ],
        "insights": {
            "yes": {
                "tone": "💡 사실은요",
                "text": (
                    "강아지는 **첫 6개월 사회화 경험**에 따라 평생 성격이 결정돼요. "
                    "주인만 보게 하면 분리불안·낯선 사람 공격성 같은 문제 행동이 생기기 쉽답니다. "
                    "이웃·다른 개·다양한 환경을 경험시켜주는 게 강아지 행복의 핵심이에요."
                ),
            },
        },
    },

    # ═══════════════ Stage 2: 시야 확장 ═══════════════
    {
        "id": "Q4_which_breed_image",
        "stage": "horizon",
        "stage_kr": "시야 확장",
        "question": "어떤 강아지를 떠올리고 계세요?",
        "options": [
            {"value": "famous",  "label": "말티즈·푸들 같은 유명 견종"},
            {"value": "around",  "label": "친구나 가족이 키우는 견종"},
            {"value": "sns",     "label": "SNS·인터넷에서 본 견종"},
            {"value": "unknown", "label": "잘 모르겠어서 추천받으러 왔어요"},
        ],
        "insights": {
            "famous": {
                "tone": "🌍 알고 계셨나요?",
                "text": (
                    "한국에서 잘 알려진 견종은 50종 정도지만, "
                    "세계에는 **300종 가까운 견종**이 있어요. "
                    "어쩌면 당신과 더 잘 맞는, **덜 유행하는 좋은 견종**이 있을지도 몰라요."
                ),
            },
            "sns": {
                "tone": "📷 짚어드려요",
                "text": (
                    "SNS에서 본 강아지의 모습은 실제와 다를 수 있어요. "
                    "귀여운 사진 뒤에 보호자의 매일 청소·산책·훈련이 있다는 것, "
                    "그리고 영상으로는 보이지 않는 짖음·체취도 함께 있다는 것을 기억해주세요."
                ),
            },
        },
    },
    {
        "id": "Q5_open_to_unique",
        "stage": "horizon",
        "stage_kr": "시야 확장",
        "question": "외국에서 인기지만 한국에선 흔치 않은 견종도 추천받는 것, 어떠세요?",
        "helper": "당신의 라이프스타일에 잘 맞는다면 시야 넓혀볼 수 있어요",
        "options": [
            {"value": "yes",  "label": "네, 시야 넓혀보고 싶어요"},
            {"value": "no",   "label": "한국에서 흔한 견종이 안심돼요"},
            {"value": "both", "label": "둘 다 보여주세요"},
        ],
        # 이 답변은 인사이트보다 추천 알고리즘에 영향 (recommendation_modifiers 참고)
    },

    # ═══════════════ Stage 3: 현실 인식 ═══════════════
    {
        "id": "Q6_long_term",
        "stage": "reality",
        "stage_kr": "현실 인식",
        "question": "강아지 평균 수명이 12~15년이에요. 10년 후 본인 라이프스타일을 그려볼 수 있으세요?",
        "options": [
            {"value": "confident", "label": "네, 평생 함께할 자신 있어요"},
            {"value": "later",     "label": "그건 그때 가서요"},
            {"value": "unknown",   "label": "잘 모르겠어요"},
        ],
        "insights": {
            "later": {
                "tone": "🌱 생각해볼게요",
                "text": (
                    "10년 후엔 직장·결혼·이사·해외이주 같은 큰 변화가 생길 수 있어요. "
                    "그때 강아지를 못 키우는 환경이 되면 어떻게 하실 건가요? "
                    "**\"그래도 끝까지\"** 라는 마음이 입양의 첫 조건이에요."
                ),
            },
            "unknown": {
                "tone": "🌱 함께 생각해봐요",
                "text": (
                    "한국 유기견의 가장 큰 원인은 보호자의 환경 변화예요. "
                    "이사·결혼·취업 같은 변화가 와도 강아지와 함께할 수 있는 환경을 "
                    "먼저 만드는 것이 입양의 시작이에요."
                ),
            },
        },
    },
    {
        "id": "Q7_senior_cost",
        "stage": "reality",
        "stage_kr": "현실 인식",
        "question": "강아지가 7세를 넘으면 관절·심장·신장 등으로 월 20만원 이상 정기 의료비가 들 수 있어요. 감당 가능하세요?",
        "options": [
            {"value": "ready",  "label": "네, 미리 준비할 수 있어요"},
            {"value": "burden", "label": "가능은 한데 부담돼요"},
            {"value": "later",  "label": "그때 가서 생각해볼게요"},
        ],
        "insights": {
            "later": {
                "tone": "💸 알고 계세요?",
                "text": (
                    "강아지의 **마지막 5년**이 평생 의료비의 70%를 차지해요. "
                    "\"그때 가서\"라고 미루면 정작 그때 결정을 내리기 가장 어려워져요. "
                    "지금부터 월 5만원씩 적금처럼 모아두시는 걸 추천드려요."
                ),
            },
        },
    },
    {
        "id": "Q8_problem_behavior",
        "stage": "reality",
        "stage_kr": "현실 인식",
        "question": "강아지가 짖거나 분리불안 등 문제 행동을 보일 때 어떻게 하실 건가요?",
        "options": [
            {"value": "train",   "label": "전문 훈련 받고 끝까지 함께해요"},
            {"value": "give_up", "label": "한계가 오면 어쩔 수 없어요"},
            {"value": "unknown", "label": "잘 모르겠어요"},
        ],
        "insights": {
            "give_up": {
                "tone": "🐾 짚어드려요",
                "text": (
                    "한국 유기견의 **가장 큰 원인은 문제 행동**이에요. "
                    "그런데 짖음·물기·분리불안은 대부분 **훈련으로 완화**돼요. "
                    "입양 전 \"끝까지 함께\"라는 결심이 흔들리면 안 됩니다. "
                    "당신이 답하기 어려우셨다면, 입양 시점을 조금 더 늦추는 것도 방법이에요."
                ),
            },
            "unknown": {
                "tone": "🐾 알려드려요",
                "text": (
                    "강아지의 문제 행동은 대부분 견종 특성·환경·훈련 부족이 원인이에요. "
                    "결과 화면에서 견종별 훈련 난이도를 보여드릴게요."
                ),
            },
        },
    },
]


# ─── 헬퍼 함수 ──────────────────────────────────────────

def questions_by_stage(stage: str) -> list[Question]:
    """특정 단계의 질문만 추출"""
    return [q for q in QUESTIONS if q["stage"] == stage]


STAGES = [
    ("myth",    "🟨", "흔한 오해 깨기"),
    ("horizon", "🟩", "시야 확장"),
    ("reality", "🟥", "현실 인식"),
]


def collect_insights(answers: dict) -> list[dict]:
    """
    사용자 답변에서 인사이트 메시지 수집.

    Returns: [{"stage_kr": str, "tone": str, "text": str}, ...]
    """
    insights = []
    for q in QUESTIONS:
        ans = answers.get(q["id"])
        if not ans:
            continue
        insight = q.get("insights", {}).get(ans)
        if insight:
            insights.append({
                "stage_kr": q["stage_kr"],
                "tone": insight["tone"],
                "text": insight["text"],
            })
    return insights


def get_recommendation_modifiers(answers: dict) -> dict:
    """
    답변에서 추천 알고리즘에 영향을 주는 변수 추출.

    Returns: {
        "include_unique": bool,         # unique tier 견종 섞을지
        "warn_about_cost": bool,        # 비용 안일하게 답한 경우 (경고 강화)
        "prefer_easy_training": bool,   # 문제행동 대처 약하다고 답한 경우
        "korean_only": bool,            # 한국 인기견종만 원하는 경우
    }
    """
    return {
        "include_unique":       answers.get("Q5_open_to_unique") in ("yes", "both"),
        "korean_only":          answers.get("Q5_open_to_unique") == "no",
        "warn_about_cost":      answers.get("Q2_monthly_cost") in ("10", "unknown"),
        "prefer_easy_training": answers.get("Q8_problem_behavior") == "give_up",
    }


def get_opening_message(answers: dict) -> str:
    """결과 화면 상단에 띄울 따뜻한 인삿말 (답변 톤 반영)"""
    # 답변 중 신중한 답이 많으면 격려, 안일한 답이 많으면 부드럽게 짚어줌
    thoughtful = 0
    careless = 0

    if answers.get("Q1_small_easy") == "no": thoughtful += 1
    elif answers.get("Q1_small_easy") == "yes": careless += 1

    if answers.get("Q3_only_owner") == "no": thoughtful += 1
    elif answers.get("Q3_only_owner") == "yes": careless += 1

    if answers.get("Q6_long_term") == "confident": thoughtful += 1
    elif answers.get("Q6_long_term") == "later": careless += 1

    if answers.get("Q7_senior_cost") == "ready": thoughtful += 1
    elif answers.get("Q7_senior_cost") == "later": careless += 1

    if answers.get("Q8_problem_behavior") == "train": thoughtful += 1
    elif answers.get("Q8_problem_behavior") == "give_up": careless += 1

    if thoughtful >= 3:
        return (
            "✨ 신중하게 답해주셨네요. "
            "강아지에 대한 책임감이 느껴져요. "
            "당신의 마음에 잘 맞을 견종을 찾아드릴게요."
        )
    elif careless >= 3:
        return (
            "🌱 함께 알아가요. "
            "강아지 입양은 큰 결정이라, 알아두시면 좋을 것들을 정리해드렸어요. "
            "한 번씩 천천히 읽어보시고, 그 다음 추천 견종도 살펴보세요."
        )
    else:
        return (
            "🐾 당신의 답을 들었어요. "
            "함께 알아두면 좋을 것들과, 라이프스타일에 맞을 견종을 함께 보여드릴게요."
        )
