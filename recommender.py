"""
견종 추천 매칭 엔진

사용자 답변(예산/산책/훈련 ± 외모) → 견종별 매칭 점수 계산.
점수 기반 정렬로 항상 결과 N개 보장 (AND 필터링의 빈 결과 문제 해결).

매칭 점수 구성 (최대 100점):
  - 예산:       30점 (사용자 예산과 견종 비용 일치 시 만점)
  - 산책 시간:  30점 (사용자 가능 시간과 권장 시간 차이 기반)
  - 훈련 의지:  30점 (사용자 의지 ≥ 견종 난이도 시 만점)
  - 한국 인기:  10점 (1~10위 +10, 11~30위 +5, 그 외 0)

외모 필터(폴백):
  - 점수에 반영하지 않고 결과에서 제외하는 방식 (hard filter)
  - 크기 / 털 길이만 매칭
"""

from __future__ import annotations
import json
from pathlib import Path


# ─── 사용자 답변 옵션 ──────────────────────────────────────────

BUDGET_OPTIONS = [
    {"label": "월 20만원 이하",      "level": "low"},
    {"label": "월 20~35만원",        "level": "medium"},
    {"label": "월 35~50만원",        "level": "high"},
    {"label": "월 50만원 이상",      "level": "very_high"},
]

WALK_OPTIONS = [
    {"label": "20분 이내",  "minutes": 20},
    {"label": "30~45분",   "minutes": 45},
    {"label": "1시간",     "minutes": 75},
    {"label": "2시간 이상", "minutes": 120},
]

TRAINING_OPTIONS = [
    {"label": "거의 어려워요 (기본 훈련도 부담)",     "willingness": 1},
    {"label": "기본 훈련 정도는 할 수 있어요",        "willingness": 3},
    {"label": "적극적으로 훈련에 시간 들일 수 있어요", "willingness": 5},
]

SIZE_OPTIONS = [
    {"label": "상관없음", "value": None},
    {"label": "소형 (작은 강아지)",  "value": "small"},
    {"label": "중형",                "value": "medium"},
    {"label": "대형/초대형",         "value": "large"},  # large+giant 합쳐서
]

COAT_LENGTH_OPTIONS = [
    {"label": "상관없음", "value": None},
    {"label": "짧은 털 (관리 쉬움)",          "value": "Short"},
    {"label": "중간 길이",                    "value": "Medium"},
    {"label": "긴 털 (예쁘지만 관리 필요)",   "value": "Long"},
]


COST_LEVEL_ORDER = ["low", "medium", "high", "very_high"]


# ─── 점수 계산 ─────────────────────────────────────────────────

def score_budget(breed: dict, user_budget_level: str) -> int:
    """예산 일치도 (최대 30점)"""
    breed_level = breed.get("cost_estimate", {}).get("level")
    if not breed_level:
        return 10  # 데이터 없으면 중간 점수

    if breed_level == user_budget_level:
        return 30

    # 한 단계 차이 = 15점
    try:
        diff = abs(COST_LEVEL_ORDER.index(breed_level) - COST_LEVEL_ORDER.index(user_budget_level))
    except ValueError:
        return 5
    if diff == 1:
        return 15
    if diff == 2:
        return 5
    return 0


def score_walk(breed: dict, user_walk_minutes: int) -> int:
    """산책 시간 매칭 (최대 30점)"""
    breed_walk = breed.get("scores", {}).get("exercise_needs", {}).get("daily_walk_minutes")
    if breed_walk is None:
        return 10

    # 사용자가 충분히 시간을 낼 수 있으면 만점
    # 사용자 시간 < 견종 권장 시간이면 차이만큼 감점
    if user_walk_minutes >= breed_walk:
        return 30

    diff = breed_walk - user_walk_minutes
    if diff <= 15: return 25
    if diff <= 30: return 18
    if diff <= 60: return 10
    return 0


def score_training(breed: dict, user_willingness: int) -> int:
    """훈련 의지 매칭 (최대 30점)

    사용자 의지 1(어려움)/3(기본)/5(적극)
    견종 difficulty 1(매우 쉬움)~5(매우 어려움)

    사용자 의지가 견종 난이도보다 높거나 같으면 만점.
    부족할수록 감점.
    """
    diff_score = breed.get("scores", {}).get("training_difficulty", {}).get("difficulty_score")
    if diff_score is None:
        return 10

    # 사용자 의지 점수와 견종 난이도 점수의 차이
    # 의지 5 + 난이도 5 = 가능 (만점)
    # 의지 1 + 난이도 5 = 매우 부족 (0점)
    gap = diff_score - user_willingness  # 양수면 사용자 의지 부족

    if gap <= 0:   return 30  # 의지 충분
    if gap <= 1:   return 20
    if gap <= 2:   return 10
    return 0


def score_popularity_bonus(breed: dict) -> int:
    """한국 인기 보너스 (최대 10점)"""
    rank = breed.get("kr_popularity_rank")
    if rank is None:
        return 0
    if rank <= 10:  return 10
    if rank <= 30:  return 5
    return 0


def compute_match_score(breed: dict, answers: dict) -> dict:
    """
    모든 요소 합산 매칭 점수 계산.

    answers: {
        "budget_level":   "low" | "medium" | "high" | "very_high",
        "walk_minutes":   int,
        "willingness":    1 | 3 | 5,
    }
    """
    s_budget = score_budget(breed, answers["budget_level"])
    s_walk = score_walk(breed, answers["walk_minutes"])
    s_train = score_training(breed, answers["willingness"])
    s_pop = score_popularity_bonus(breed)

    total = s_budget + s_walk + s_train + s_pop
    return {
        "total": total,
        "percent": round(total / 100 * 100),
        "breakdown": {
            "budget": s_budget,
            "walk":   s_walk,
            "training": s_train,
            "popularity_bonus": s_pop,
        }
    }


# ─── 외모 필터 (폴백, hard filter) ─────────────────────────────

def passes_appearance_filter(breed: dict, size_pref: str | None, coat_len_pref: str | None) -> bool:
    """
    외모 선호 통과 여부. None이면 그 항목은 패스.

    size_pref: "small" | "medium" | "large" | None
    coat_len_pref: "Short" | "Medium" | "Long" | None
    """
    if size_pref:
        breed_size = breed.get("size_category")
        # "large" 선택 시 large + giant 둘 다 매칭
        if size_pref == "large":
            if breed_size not in ("large", "giant"):
                return False
        else:
            if breed_size != size_pref:
                return False

    if coat_len_pref:
        coat_lens = breed.get("traits", {}).get("coat_length", [])
        if not isinstance(coat_lens, list) or coat_len_pref not in coat_lens:
            return False

    return True


# ─── 메인 추천 함수 ───────────────────────────────────────────

def recommend(
    breeds: list[dict],
    answers: dict,
    appearance: dict | None = None,
    top_n: int = 12,
    only_korean_popular: bool = True,
    journey_modifiers: dict | None = None,
) -> list[dict]:
    """
    답변 기반 견종 추천.

    answers: {budget_level, walk_minutes, willingness}
    appearance: {size, coat_length} (선택)
    only_korean_popular: True면 한국 인기 50위 내(popular+less_popular)에서만 추천
                        False면 unique까지 포함
    journey_modifiers: 3단계 여정 답변 기반 가중치 조정 (journey.get_recommendation_modifiers 결과)
                       {include_unique, korean_only, warn_about_cost, prefer_easy_training}
    """
    journey_modifiers = journey_modifiers or {}

    # ── journey 답변에 따라 only_korean_popular 자동 조정 ──
    if journey_modifiers.get("include_unique"):
        only_korean_popular = False  # unique 견종 풀에 포함
    elif journey_modifiers.get("korean_only"):
        only_korean_popular = True

    # 1차: 한국 인기 견종 풀로 한정 (입양 희망자 베이스라인)
    if only_korean_popular:
        pool = [b for b in breeds if b.get("kr_popularity_tier") in ("popular", "less_popular")]
    else:
        pool = breeds

    # 2차: 외모 필터 적용
    if appearance:
        size = appearance.get("size")
        coat = appearance.get("coat_length")
        pool = [b for b in pool if passes_appearance_filter(b, size, coat)]

    # 변종 그룹 중복 제거 (Poodle 3종 중 매칭 점수 가장 높은 1개만)
    # → 카드 그리드에 푸들이 3번 나오는 걸 방지

    # 3차: 점수 계산 (journey modifier 가중치 반영)
    scored = []
    for b in pool:
        s = compute_match_score(b, answers)
        # 훈련 한계 답한 사용자에겐 훈련 쉬운 견종에 보너스
        if journey_modifiers.get("prefer_easy_training"):
            train = b.get("scores", {}).get("training_difficulty", {}).get("difficulty_score", 5)
            if train <= 2:
                s["total"] += 8
                s["percent"] = round(s["total"] / 100 * 100)
        scored.append({**b, "_match": s})

    # 4차: 변종 그룹 dedupe
    seen_groups = {}
    unique_results = []
    for b in scored:
        vg = b.get("variety_group") or b["_id"]
        if vg in seen_groups:
            # 이미 같은 그룹이 있으면 점수 높은 쪽 유지
            if b["_match"]["total"] > seen_groups[vg]["_match"]["total"]:
                # 교체
                idx = unique_results.index(seen_groups[vg])
                unique_results[idx] = b
                seen_groups[vg] = b
        else:
            seen_groups[vg] = b
            unique_results.append(b)

    # 5차: 점수 내림차순 정렬, 상위 N개
    unique_results.sort(key=lambda b: -b["_match"]["total"])
    final = unique_results[:top_n]

    # 6차: 시야 확장 — Q5 "시야 넓혀보고 싶어요" 답한 경우
    # 결과 안에 unique tier 견종이 없으면 상위 unique 견종 1~2마리를 강제 포함 (마지막 자리)
    if journey_modifiers.get("include_unique"):
        already_has_unique = any(b.get("kr_popularity_tier") == "unique" for b in final)
        if not already_has_unique:
            unique_tier_only = [
                b for b in unique_results
                if b.get("kr_popularity_tier") == "unique"
            ][:2]
            for b in unique_tier_only:
                b["_horizon_pick"] = True   # UI에서 "시야 확장 추천" 뱃지용
            # 결과 맨 뒤에 추가 (top_n 내에서)
            final = final[:top_n - len(unique_tier_only)] + unique_tier_only

    return final


def load_breeds(json_path: str | Path) -> list[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["breeds"]
