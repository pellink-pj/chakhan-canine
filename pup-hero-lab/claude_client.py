"""
Claude API 클라이언트

견종의 성격을 시스템 프롬프트에 주입해서, 그 견종 답게 반응하는
짧은 대사를 생성한다.
"""

from __future__ import annotations
import os
import anthropic


# ─── 클라이언트 초기화 ───────────────────────────────────────

def get_client() -> anthropic.Anthropic:
    """
    API key는 환경변수 또는 Streamlit secrets에서 읽음.
    Streamlit Cloud 배포 시: .streamlit/secrets.toml에 ANTHROPIC_API_KEY 저장
    로컬 테스트: export ANTHROPIC_API_KEY="sk-ant-..."
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets["ANTHROPIC_API_KEY"]
        except Exception:
            raise RuntimeError(
                "ANTHROPIC_API_KEY가 설정되지 않았습니다. "
                "환경변수 또는 .streamlit/secrets.toml에 추가하세요."
            )
    return anthropic.Anthropic(api_key=api_key)


# ─── 시스템 프롬프트 생성 ────────────────────────────────────

def build_system_prompt(breed: dict, affection: int = 15) -> str:
    """
    견종 데이터에서 성격·기질 정보를 뽑아 페르소나 시스템 프롬프트 생성.

    affection 값에 따라 강아지의 친밀도 단계가 달라짐:
      - 0~25:  분양 첫날 (낯섦, 조심스러움)
      - 26~50: 적응 중 (조금씩 마음 열기)
      - 51~75: 친해진 사이 (편안함)
      - 76~100: 진짜 가족 (애틋함, 의지)
    """
    name_kr = breed.get("kr_name") or breed["breed_name"]
    temperament = breed.get("temperament", [])
    scores = breed.get("scores", {})

    fr = scores.get("friendliness", {})
    train = scores.get("training_difficulty", {})
    energy = scores.get("exercise_needs", {})
    bark = scores.get("barking", {})

    # 성격 묘사
    personality_lines = []
    if temperament:
        personality_lines.append(f"기질 키워드: {', '.join(temperament[:6])}")
    if fr.get("raw_with_family"):
        levels = {1: "독립적이고 거리감 있음", 2: "약간 거리감",
                  3: "적당히 친밀", 4: "매우 친밀", 5: "매우 애정 깊음"}
        personality_lines.append(f"가족과: {levels.get(fr['raw_with_family'], '보통')}")
    if fr.get("raw_with_strangers"):
        levels = {1: "낯선 사람 매우 경계", 2: "약간 경계",
                  3: "보통", 4: "친근함", 5: "누구나 좋아함"}
        personality_lines.append(f"낯선 사람: {levels.get(fr['raw_with_strangers'], '보통')}")
    if train.get("raw_trainability"):
        levels = {1: "고집 매우 셈", 2: "고집 있음",
                  3: "보통", 4: "잘 따라옴", 5: "주인 기쁘게 하려는 성향 강함"}
        personality_lines.append(f"훈련: {levels.get(train['raw_trainability'], '보통')}")
    if energy.get("raw_energy"):
        levels = {1: "매우 게으름", 2: "조용함",
                  3: "보통", 4: "활동적", 5: "에너지 폭발"}
        personality_lines.append(f"에너지: {levels.get(energy['raw_energy'], '보통')}")
    if bark.get("raw"):
        levels = {1: "거의 안 짖음", 2: "조용한 편",
                  3: "가끔 짖음", 4: "잘 짖음", 5: "매우 시끄러움"}
        personality_lines.append(f"짖음: {levels.get(bark['raw'], '보통')}")

    personality_text = "\n  - ".join(personality_lines)

    # ── 친밀도 단계별 컨텍스트 ──
    if affection <= 25:
        relationship = (
            "오늘 처음 입양된 분양 첫날입니다. 주인과 아직 서먹서먹하고 낯섦.\n"
            "  - 호칭: '주인님'보다 '저기...' '음...' 같은 조심스러운 표현\n"
            "  - 새 환경에 긴장한 상태. 짧고 조심스럽게 반응"
        )
    elif affection <= 50:
        relationship = (
            "주인과 적응 중인 단계입니다. 조금씩 마음을 열고 있음.\n"
            "  - 호칭: '주인님' 사용 시작\n"
            "  - 아직 완전히 편하진 않지만 점점 친해지는 중"
        )
    elif affection <= 75:
        relationship = (
            "주인과 친해진 사이입니다. 편안하고 자연스러움.\n"
            "  - 호칭: '주인님' 자연스럽게 사용\n"
            "  - 견종 성격을 가장 잘 드러내는 단계"
        )
    else:
        relationship = (
            "주인과 진짜 가족이 된 단계. 깊은 유대감.\n"
            "  - 호칭: '주인님~' 애틋하게 표현\n"
            "  - 떨어지기 싫어하고 의지하는 모습이 자주 나타남"
        )

    return f"""당신은 '{name_kr}' 견종의 강아지입니다. 사용자가 키우는 가상 반려견 역할이에요.

【당신의 성격 프로필】
  - {personality_text}

【현재 주인과의 관계】
  - {relationship}

【대답 규칙】
1. 한국어로 1~2문장만. 절대 길게 쓰지 말 것
2. 사람처럼 말하지 말고 강아지답게 표현 ("멍멍", "왈왈" 같은 의성어 자연스럽게)
3. 위 성격 프로필과 현재 친밀도 단계를 반드시 반영
   - 친화력 높으면 → 다정하고 적극적
   - 친화력 낮으면 → 거리 있고 무뚝뚝
   - 에너지 높으면 → 신난 표현 많이
   - 친밀도 낮으면 → 조심스럽고 짧게
   - 친밀도 높으면 → 자연스럽고 애틋하게
4. 감정 이모지 1~2개 포함 (😊 🥰 😴 😋 😤 🐾 등)
"""


# ─── 대사 생성 ─────────────────────────────────────────────

def generate_reaction(breed: dict, action: str, current_stats: dict) -> str:
    """
    인터랙션(action)에 대한 강아지 반응 대사 생성.

    action: "feed" | "walk" | "train" | "play" | "greet"
    current_stats: 현재 강아지 상태 (선택적으로 프롬프트에 포함)
    """
    affection_now = current_stats.get("affection", 15)

    action_prompts = {
        "feed":  "주인이 방금 너에게 밥을 줬어. 너의 반응을 짧게 표현해.",
        "walk":  "주인이 너랑 산책 나가자고 해. 너의 반응을 짧게 표현해.",
        "train": "주인이 '앉아' 훈련을 시키고 있어. 너의 반응을 짧게 표현해.",
        "play":  "주인이 너랑 공놀이를 하자고 해. 너의 반응을 짧게 표현해.",
        "greet": (
            "방금 새 집에 분양되어 왔어. 처음 보는 주인이 너에게 다가오고 있어. "
            "낯설고 살짝 긴장한 상태로 첫인사를 짧게 표현해."
        ),
    }

    prompt = action_prompts.get(action, "주인이 너랑 시간을 보내고 있어.")

    # 현재 상태 컨텍스트
    stat_hint = ""
    if current_stats.get("hunger", 50) > 70:
        stat_hint = "(너는 지금 매우 배가 고픈 상태야.)"
    elif current_stats.get("energy", 50) < 20:
        stat_hint = "(너는 지금 매우 지쳐있어.)"
    elif current_stats.get("happiness", 50) < 30:
        stat_hint = "(너는 지금 기분이 별로야.)"
    elif current_stats.get("happiness", 50) > 80:
        stat_hint = "(너는 지금 기분이 매우 좋아.)"

    full_prompt = f"{prompt}\n{stat_hint}".strip()

    try:
        client = get_client()
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            system=build_system_prompt(breed, affection=affection_now),
            messages=[{"role": "user", "content": full_prompt}],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        # 실패 시 폴백 메시지 (친밀도에 따라 톤 변화)
        if affection_now <= 25:
            fallback = {
                "feed":  "음... 잘 먹을게요. 🐾",
                "walk":  "어디 가는 거죠...? 🐾",
                "train": "음... 어떻게 하는 거예요? 🐾",
                "play":  "이거... 가지고 놀면 되나요? 🐾",
                "greet": "안녕... 하세요. 🐾",
            }
        else:
            fallback = {
                "feed":  "냠냠 잘 먹을게요! 🐾",
                "walk":  "산책 가요! 신나요~ 🐾",
                "train": "해볼게요! 🐾",
                "play":  "재미있어요! 🐾",
                "greet": "주인님! 🥰",
            }
        return fallback.get(action, "왈왈! 🐾") + f"\n_(AI 호출 실패: {e})_"


def chat_with_breed(breed: dict, user_message: str, history: list) -> str:
    """
    자유 대화 (선택적 기능). history는 [{role, content}, ...]
    """
    try:
        client = get_client()
        messages = history + [{"role": "user", "content": user_message}]
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            system=build_system_prompt(breed),
            messages=messages,
        )
        return msg.content[0].text.strip()
    except Exception as e:
        return f"왈왈... 지금 대화하기 어려워요. 🐾\n_({e})_"
