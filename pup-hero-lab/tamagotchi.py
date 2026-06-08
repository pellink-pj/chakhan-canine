"""
다마고치 게임 로직

스탯 시스템 + 인터랙션이 스탯에 미치는 영향.
견종 데이터의 scores(traits)에 따라 변화 폭이 달라짐.
"""

from __future__ import annotations
from typing import Literal


# ─── 초기 스탯 (분양 첫날 컨셉) ─────────────────────────────
# 모든 견종이 똑같이 "낯선 환경에 막 왔다" 상태로 시작.
# 친화력 높은 견종일수록 인터랙션을 통해 친밀도가 더 빨리 올라간다 (apply_action 참고).

INITIAL_STATS = {
    "happiness":  55,   # 행복도 — 약간 긴장, 어색함
    "hunger":     30,   # 배고픔 (이건 견종 무관)
    "energy":     65,   # 에너지 — 낯선 곳에서 약간 위축
    "affection":  15,   # 친밀도 — 처음 만난 사이라 매우 낮음
}

STAT_MAX = 100
STAT_MIN = 0

STAT_LABELS_KR = {
    "happiness": ("행복도", "😊"),
    "hunger":    ("배고픔", "🍖"),
    "energy":    ("에너지", "⚡"),
    "affection": ("친밀도", "💖"),
}


# ─── 인터랙션 정의 ─────────────────────────────────────────

Action = Literal["feed", "walk", "train", "play", "greet"]


def apply_action(stats: dict, action: Action, breed: dict) -> dict:
    """
    인터랙션이 스탯에 미치는 영향을 계산.
    견종의 traits에 따라 효과가 달라짐.

    🔑 핵심: 친밀도(affection)는 친화력 점수로 가중됨.
    친화력 5.0 견종(골든)은 친화력 2.0 견종(진돗개)보다 약 2.5배 빨리 친해진다.
    """
    new_stats = stats.copy()
    scores = breed.get("scores", {})
    energy_score = scores.get("exercise_needs", {}).get("raw_energy", 3)
    train_score = scores.get("training_difficulty", {}).get("raw_trainability", 3)
    friendliness = scores.get("friendliness", {}).get("avg_score", 3.0)

    # ── 친밀도 증가 가중 계수 ──
    # 친화력 3.0 = 1.0배 (기본)
    # 친화력 5.0 = 1.67배 (빠르게 친해짐)
    # 친화력 2.0 = 0.67배 (천천히 친해짐)
    affection_mult = friendliness / 3.0

    def gain_affection(base: float) -> int:
        """친화력 기반 친밀도 증가량 계산"""
        return int(round(base * affection_mult))

    if action == "feed":
        # 먹이 → 배고픔 ↓, 행복도 약간 ↑
        new_stats["hunger"] -= 35
        new_stats["happiness"] += 10
        new_stats["affection"] += gain_affection(3)

    elif action == "walk":
        # 산책 → 에너지 ↓, 행복도 ↑, 친밀도 ↑
        # 에너지 높은 견종일수록 산책 효과 큼 (행복도)
        walk_joy = 15 + (energy_score - 3) * 5
        new_stats["energy"] -= 15 + max(0, (energy_score - 3) * 3)
        new_stats["happiness"] += walk_joy
        new_stats["affection"] += gain_affection(8)
        new_stats["hunger"] += 8

    elif action == "train":
        # 훈련 → 에너지 ↓, 친밀도 ↑
        # 훈련 잘 따라오는 견종일수록 친밀도 효과 큼
        # 훈련 안 따라오는 견종은 행복도 살짝 감소
        new_stats["energy"] -= 12
        new_stats["affection"] += gain_affection(5 + train_score * 1.5)
        new_stats["hunger"] += 5
        if train_score <= 2:
            new_stats["happiness"] -= 5  # 고집 센 견종은 훈련 싫어함
        else:
            new_stats["happiness"] += 5

    elif action == "play":
        # 놀이 → 행복도 ↑, 에너지 ↓, 친밀도 ↑
        play_joy = 12 + int(friendliness * 3)
        new_stats["happiness"] += play_joy
        new_stats["energy"] -= 10
        new_stats["affection"] += gain_affection(5)
        new_stats["hunger"] += 4

    elif action == "greet":
        # 인사 → 친밀도 ↑, 행복도 살짝 ↑
        new_stats["affection"] += gain_affection(3)
        new_stats["happiness"] += 3

    # 0~100 범위 클램프
    for k in new_stats:
        new_stats[k] = max(STAT_MIN, min(STAT_MAX, new_stats[k]))

    return new_stats


# ─── 시간 경과 (passive decay) ─────────────────────────────

def passive_decay(stats: dict, minutes_passed: int, breed: dict) -> dict:
    """
    시간이 흐르면 자연스럽게 스탯 변화.
    배고픔 ↑, 행복도 ↓, 에너지 ↑ (회복).
    견종 특성에 따라 감소 속도 다름.
    """
    new_stats = stats.copy()
    scores = breed.get("scores", {})
    energy_score = scores.get("exercise_needs", {}).get("raw_energy", 3)

    # 분당 변화량
    hunger_per_min = 0.5   # 10분에 +5
    happiness_per_min = 0.3
    energy_per_min = 0.4   # 시간 흐르면 에너지 회복 (잠 잔다고 가정)

    # 에너지 높은 견종일수록 행복도 더 빨리 감소 (심심해함)
    happiness_loss_multiplier = 1 + (energy_score - 3) * 0.15

    new_stats["hunger"]    += hunger_per_min * minutes_passed
    new_stats["happiness"] -= happiness_per_min * minutes_passed * happiness_loss_multiplier
    new_stats["energy"]    += energy_per_min * minutes_passed

    # 친밀도는 천천히 감소 (오래 안 보면 멀어짐)
    new_stats["affection"] -= 0.1 * minutes_passed

    for k in new_stats:
        new_stats[k] = max(STAT_MIN, min(STAT_MAX, new_stats[k]))

    return new_stats


# ─── 현재 기분/상태 표현 ─────────────────────────────────────

def get_mood(stats: dict) -> tuple[str, str]:
    """
    현재 스탯을 보고 강아지의 기분/표정 이모지와 한 줄 설명 반환.
    """
    happiness = stats["happiness"]
    hunger = stats["hunger"]
    energy = stats["energy"]
    affection = stats["affection"]

    # 우선순위: 위급 → 일반
    if hunger >= 85:
        return "😩", "너무 배고파요... 밥 주세요!"
    if energy <= 15:
        return "😴", "너무 졸려요... 쉴래요."
    if happiness <= 20:
        return "😢", "기분이 너무 안 좋아요..."
    if affection <= 15:
        return "😐", "주인님이랑 좀 멀어진 것 같아요..."

    if happiness >= 80 and affection >= 70:
        return "🥰", "주인님이랑 너무 행복해요!"
    if happiness >= 70:
        return "😊", "기분 좋아요!"
    if energy >= 80:
        return "🤸", "신나서 뛰어다니고 싶어요!"

    return "🐶", "보통이에요."


def get_stat_color(value: int) -> str:
    """progress bar 색상 결정 (Streamlit용)"""
    if value >= 70:  return "normal"
    if value >= 40:  return "normal"
    return "off"
