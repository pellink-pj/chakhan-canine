"""
견종별 희망 메시지 생성 (멍메이트 핵심 가치 반영)

기존 접근: "⚠️ 이 견종은 짖음이 많아요" (단순 경고)
멍메이트 접근: "🔊 원래 잘 짖지만, 훈련으로 컨트롤 가능해요" (희망 + 솔루션)

견종의 부정적 특성(짖음, 물기, 분리불안)을 단순 경고가 아니라
**훈련 가능성과 결합한 희망 메시지**로 변환.

핵심 인사이트:
  창업자의 셸티는 짖음 5/5(매우 높음)인 견종이지만,
  5년 훈련으로 짖지 않고 물지 않고 자극에도 인내하는 강아지가 되었음.
  → "좋은 견종이 따로 있는 게 아니라, 좋은 보호자가 만든다"
"""

from __future__ import annotations


# 셸티 같은 살아있는 사례 — 메시지에 인용
FOUNDER_TESTIMONY = (
    "💡 멍메이트 창업자의 셸티도 짖음 매우 높은 견종이에요. "
    "5년 훈련으로 지금은 짖지 않고, 물지 않고, "
    "아이가 와서 눈을 찔러도 가만히 있어요."
)


def get_trait_messages(breed: dict) -> list[dict]:
    """
    견종의 특성을 멍메이트 톤(훈련 희망)으로 메시지화.

    Returns: [{"icon": str, "title": str, "tone": "good"|"hope"|"caution", "text": str}, ...]
      - good:    그대로도 좋은 특성
      - hope:    원래 부담스럽지만 훈련으로 극복 가능
      - caution: 신중히 고려할 부분
    """
    messages = []
    scores = breed.get("scores", {})

    bark = scores.get("barking", {}).get("raw")
    shed = scores.get("shedding", {}).get("raw")
    train = scores.get("training_difficulty", {}).get("raw_trainability")
    energy = scores.get("exercise_needs", {}).get("raw_energy")
    friendliness = scores.get("friendliness", {})
    aff_family = friendliness.get("raw_with_family")
    with_kids = friendliness.get("raw_with_children")
    with_dogs = friendliness.get("raw_with_dogs")

    # ─── 짖음 × 훈련 가능성 ─────────────────────────────────
    if bark is not None and train is not None:
        if bark >= 4 and train >= 4:
            messages.append({
                "icon": "🔊",
                "title": "원래 잘 짖지만, 훈련으로 컨트롤 가능해요",
                "tone": "hope",
                "text": (
                    f"이 견종은 타고난 경계심으로 짖음이 많은 편이에요. "
                    f"하지만 학습 의지가 강해서, 꾸준한 훈련으로 짖음을 컨트롤할 수 있어요. "
                    f"공동주택에서도 충분히 함께 살 수 있는 견종입니다."
                ),
            })
        elif bark >= 4 and train <= 2:
            messages.append({
                "icon": "⚠️",
                "title": "짖음이 많고 훈련이 쉽지 않은 견종이에요",
                "tone": "caution",
                "text": (
                    f"짖음이 매우 잦은 편인데, 고집이 있어 훈련이 쉽지 않아요. "
                    f"공동주택 거주자라면 전문 훈련사와 함께 계획적으로 접근해야 하고, "
                    f"입양 전에 한 번 더 신중히 고민해보세요."
                ),
            })
        elif bark <= 2:
            messages.append({
                "icon": "🤫",
                "title": "조용한 견종이에요",
                "tone": "good",
                "text": "타고나길 짖음이 적은 편이라 공동주택 거주에 부담이 적어요.",
            })

    # ─── 털 빠짐 × 그루밍 ─────────────────────────────────
    if shed is not None:
        if shed >= 4:
            messages.append({
                "icon": "🐕‍🦺",
                "title": "털이 많이 빠지는 편이에요",
                "tone": "hope",
                "text": (
                    "이중모로 털 빠짐이 많은 편이에요. 매일 빗질과 정기적인 청소가 필요해요. "
                    "단, 정기 그루밍 루틴이 잡히면 옷·가구에 묻는 정도는 충분히 관리할 수 있어요."
                ),
            })
        elif shed <= 2:
            messages.append({
                "icon": "✨",
                "title": "털 빠짐이 적은 견종이에요",
                "tone": "good",
                "text": "옷·가구에 털이 잘 안 묻어요. 알러지가 있는 분에게도 비교적 적합해요.",
            })

    # ─── 친화력 × 아이 × 사회성 ─────────────────────────
    if with_kids is not None and aff_family is not None:
        if with_kids >= 4 and aff_family >= 4:
            messages.append({
                "icon": "👨‍👩‍👧",
                "title": "아이와 가족에게 다정한 견종이에요",
                "tone": "good",
                "text": (
                    "가족과의 친밀도가 높고, 어린 자녀와도 잘 어울려요. "
                    "안전하게 함께 살 수 있는 가족견 후보예요."
                ),
            })
        elif with_kids is not None and with_kids <= 2:
            messages.append({
                "icon": "🚸",
                "title": "어린 자녀가 있으시면 신중히 고려해주세요",
                "tone": "caution",
                "text": (
                    "어린 자녀와 함께 살기엔 주의가 필요한 견종이에요. "
                    "사회화 훈련과 보호자의 적극적 관리가 필수예요."
                ),
            })

    # ─── 에너지 × 운동 가능성 ────────────────────────
    if energy is not None:
        if energy >= 4:
            messages.append({
                "icon": "🏃",
                "title": "활동량이 많은 견종이에요",
                "tone": "hope",
                "text": (
                    "에너지가 높은 견종이라 하루 1시간 이상의 산책·놀이가 필요해요. "
                    "충분히 운동시켜주면 실내에선 차분히 지내요. "
                    "운동 부족 시 파괴 행동·문제 짖음이 생길 수 있어요."
                ),
            })
        elif energy <= 2:
            messages.append({
                "icon": "🛋",
                "title": "차분하고 활동량이 적은 견종이에요",
                "tone": "good",
                "text": "짧은 산책과 실내 놀이로도 만족해요. 아파트 거주자에게 적합해요.",
            })

    # ─── 다른 강아지 친화력 ──────────────────────────
    if with_dogs is not None:
        if with_dogs >= 4:
            messages.append({
                "icon": "🐶",
                "title": "다른 강아지와 잘 어울려요",
                "tone": "good",
                "text": "다견 가정이나 강아지 놀이터에 데려가도 무리 없이 어울려요.",
            })
        elif with_dogs <= 2:
            messages.append({
                "icon": "🐕",
                "title": "다른 강아지와의 만남은 천천히",
                "tone": "caution",
                "text": (
                    "다른 강아지에게 경계심을 가질 수 있어요. "
                    "어릴 때부터 다양한 견종과 만나는 사회화 훈련이 중요해요."
                ),
            })

    return messages


def get_training_overcomeable(breed: dict) -> bool:
    """
    이 견종이 '훈련으로 부정 특성을 극복할 수 있는' 케이스인지 판정.
    부정 특성(짖음·문제행동 가능성) 있지만 trainability가 높으면 True.
    """
    scores = breed.get("scores", {})
    bark = scores.get("barking", {}).get("raw", 3)
    train = scores.get("training_difficulty", {}).get("raw_trainability", 3)
    return bark >= 4 and train >= 4


def get_founder_message_if_relevant(breed: dict) -> str | None:
    """
    창업자 셸티 사례가 관련 있는 견종에만 메시지 표시.
    짖음 높고 + 훈련 가능 견종에만 (셸티 본인과 비슷한 패턴).
    """
    if get_training_overcomeable(breed):
        return FOUNDER_TESTIMONY
    return None
