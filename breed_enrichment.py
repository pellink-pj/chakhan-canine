"""
견종 데이터 enrichment 모듈

AKC 원본 traits에서 한국 사용자에게 의미 있는 파생 데이터를 생성:
  - scores: 털날림/짖음/훈련강도/운동량/친화력 등급화
  - cost_estimate: 한국 시장 월 비용 추정 (KRW + 등급)
  - lifestyle_tags: 추천 알고리즘 필터용 불리언 태그
  - rag_chunks: 벡터 임베딩용 한국어 자연어 청크
"""

from __future__ import annotations
from typing import Any


# ─── 등급 매핑 ─────────────────────────────────────────────────

LEVEL_BY_SCORE_5 = {1: "very_low", 2: "low", 3: "medium", 4: "high", 5: "very_high"}
LEVEL_KR = {
    "very_low":  "매우 낮음",
    "low":       "낮음",
    "medium":    "보통",
    "high":      "높음",
    "very_high": "매우 높음",
}


def _get_trait(traits: dict, key: str) -> int | None:
    """traits 딕셔너리에서 점수 안전 추출 (1~5 정수만 반환)"""
    v = traits.get(key)
    if isinstance(v, int) and 1 <= v <= 5:
        return v
    return None


# ─── 견종 크기 분류 ────────────────────────────────────────────

def classify_size(weight_min: Any, weight_max: Any) -> str:
    """
    체중(lb) 평균으로 크기 분류.
      small(소형):  ~22lb (10kg)
      medium(중형): 22~55lb (10~25kg)
      large(대형):  55~100lb (25~45kg)
      giant(초대형): 100lb+ (45kg+)
    """
    try:
        avg_lb = (float(weight_min) + float(weight_max)) / 2
    except (TypeError, ValueError):
        return "unknown"
    if avg_lb < 22:   return "small"
    if avg_lb < 55:   return "medium"
    if avg_lb < 100:  return "large"
    return "giant"


SIZE_KR = {"small": "소형", "medium": "중형", "large": "대형", "giant": "초대형", "unknown": "미상"}


# ─── 단위 변환 (lb→kg, inch→cm) ──────────────────────────────

def lb_to_kg(lb: Any) -> float | None:
    try:
        return round(float(lb) * 0.453592, 1)
    except (TypeError, ValueError):
        return None


def inch_to_cm(inch: Any) -> float | None:
    try:
        return round(float(inch) * 2.54, 1)
    except (TypeError, ValueError):
        return None


def build_size_display_kr(
    weight_kg_min: float | None,
    weight_kg_max: float | None,
    height_cm_min_m: float | None,
    height_cm_max_m: float | None,
    height_cm_min_f: float | None,
    height_cm_max_f: float | None,
) -> dict:
    """체중/키를 한국어 표현으로. 예: '약 2~3kg', '키 20~25cm'"""
    out = {}

    if weight_kg_min and weight_kg_max:
        if abs(weight_kg_min - weight_kg_max) < 0.5:
            out["weight_kr"] = f"약 {weight_kg_min}kg"
        else:
            out["weight_kr"] = f"{weight_kg_min}~{weight_kg_max}kg"
    elif weight_kg_max:
        out["weight_kr"] = f"{weight_kg_max}kg 이하"
    elif weight_kg_min:
        out["weight_kr"] = f"{weight_kg_min}kg 이상"

    # 키: 수컷/암컷 중 더 넓은 범위로 통합 표현
    h_mins = [h for h in [height_cm_min_m, height_cm_min_f] if h]
    h_maxs = [h for h in [height_cm_max_m, height_cm_max_f] if h]
    if h_mins and h_maxs:
        lo, hi = min(h_mins), max(h_maxs)
        if abs(lo - hi) < 1:
            out["height_kr"] = f"약 {lo}cm"
        else:
            out["height_kr"] = f"{lo}~{hi}cm"

    return out


# ─── 1. 핵심 점수 카테고리 ───────────────────────────────────

def compute_scores(traits: dict) -> dict:
    """
    AKC traits 점수에서 추천 시스템용 등급 카테고리 생성.
    """
    out = {}

    # 털날림
    s = _get_trait(traits, "shedding_level")
    if s is not None:
        out["shedding"] = {
            "raw": s,
            "level": LEVEL_BY_SCORE_5[s],
            "level_kr": LEVEL_KR[LEVEL_BY_SCORE_5[s]],
        }

    # 짖음
    s = _get_trait(traits, "barking_level")
    if s is not None:
        out["barking"] = {
            "raw": s,
            "level": LEVEL_BY_SCORE_5[s],
            "level_kr": LEVEL_KR[LEVEL_BY_SCORE_5[s]],
        }

    # 그루밍 빈도
    s = _get_trait(traits, "coat_grooming_frequency")
    if s is not None:
        # 1=Monthly, 3=Weekly, 5=Daily
        freq_kr = {1: "월 1회", 2: "2주 1회", 3: "주 1회", 4: "주 2~3회", 5: "매일"}
        out["grooming"] = {
            "raw": s,
            "level": LEVEL_BY_SCORE_5[s],
            "level_kr": LEVEL_KR[LEVEL_BY_SCORE_5[s]],
            "frequency_kr": freq_kr[s],
        }

    # 운동량 = energy_level + mental_stimulation_needs 평균
    energy = _get_trait(traits, "energy_level")
    mental = _get_trait(traits, "mental_stimulation_needs")
    if energy is not None:
        # 일일 산책 시간 추정
        walk_min = {1: 20, 2: 30, 3: 45, 4: 75, 5: 120}[energy]
        # 종합 운동 필요도 (energy 80% + mental 20%)
        combined = energy if mental is None else (energy * 0.7 + mental * 0.3)
        combined_level = LEVEL_BY_SCORE_5[round(combined)]
        out["exercise_needs"] = {
            "raw_energy": energy,
            "raw_mental_stimulation": mental,
            "level": combined_level,
            "level_kr": LEVEL_KR[combined_level],
            "daily_walk_minutes": walk_min,
        }

    # 훈련 강도 = trainability 그대로 역수 매핑
    # trainability 점수만 기반 — 학습 자체 난이도
    # mental_stimulation은 별도 차원 (정신 자극 필요량)으로 메시지에서 따로 다룸
    train = _get_trait(traits, "trainability_level")
    if train is not None:
        # 어려움 점수 = (6 - trainability)
        # trainability 5점(매우 똑똑) → difficulty 1점(매우 쉬움)
        # trainability 1점(고집) → difficulty 5점(매우 어려움)
        difficulty = max(1, min(5, 6 - train))
        out["training_difficulty"] = {
            "raw_trainability": train,
            "raw_mental_stimulation": mental,
            "difficulty_score": difficulty,
            "level": LEVEL_BY_SCORE_5[difficulty],
            "level_kr": LEVEL_KR[LEVEL_BY_SCORE_5[difficulty]],
            "note": _training_note(train, mental),
        }

    # 친화력 (한국 아파트 환경 핵심 지표)
    aff = _get_trait(traits, "affectionate_with_family")
    open_s = _get_trait(traits, "openness_to_strangers")
    other = _get_trait(traits, "good_with_other_dogs")
    kids = _get_trait(traits, "good_with_young_children")
    if aff or open_s or other or kids:
        vals = [v for v in [aff, open_s, other, kids] if v is not None]
        avg = sum(vals) / len(vals)
        level = LEVEL_BY_SCORE_5[round(avg)]
        out["friendliness"] = {
            "raw_with_family":   aff,
            "raw_with_strangers": open_s,
            "raw_with_dogs":     other,
            "raw_with_children": kids,
            "avg_score":         round(avg, 1),
            "level":             level,
            "level_kr":          LEVEL_KR[level],
        }

    return out


def _training_note(trainability: int, mental: int | None) -> str:
    """훈련 난이도에 대한 한국어 설명"""
    if trainability >= 4:
        if mental and mental >= 4:
            return "지능이 높고 학습 의지 강함. 단, 자극 부족 시 문제 행동 가능"
        return "학습 의지가 강해 훈련이 수월함"
    if trainability >= 3:
        return "꾸준한 반복 훈련 필요. 일반적 수준"
    return "독립심 강하고 고집이 있어 전문 훈련 권장"


# ─── 2. 비용 추정 ──────────────────────────────────────────────

# 한국 시장 기준 월 비용 (원). 2025년 평균 추정치.
FOOD_COST_BY_SIZE = {
    "small":  50_000,
    "medium": 90_000,
    "large":  150_000,
    "giant":  220_000,
    "unknown": 90_000,
}

# 그루밍 빈도(1~5) × 크기에 따른 월 비용
GROOMING_COST = {
    # (grooming_score, size) → 월 KRW
    1: {"small": 5_000,  "medium": 10_000, "large": 15_000, "giant": 20_000},  # 월 1회 셀프
    2: {"small": 15_000, "medium": 25_000, "large": 35_000, "giant": 45_000},
    3: {"small": 30_000, "medium": 50_000, "large": 70_000, "giant": 90_000},  # 주 1회
    4: {"small": 50_000, "medium": 80_000, "large": 100_000,"giant": 130_000},
    5: {"small": 70_000, "medium": 110_000,"large": 140_000,"giant": 170_000}, # 매일 + 정기 미용
}


# 단두종 (호흡기 문제 위험) — breed_url_key 기준
BRACHYCEPHALIC_BREEDS = {
    "bulldog",
    "french-bulldog",
    "pug",
    "boston-terrier",
    "pekingese",
    "shih-tzu",
    "boxer",
    "bullmastiff",
    "cavalier-king-charles-spaniel",
    "japanese-chin",
    "lhasa-apso",
    "chow-chow",
    "dogue-de-bordeaux",
    "neapolitan-mastiff",
}

# 척추/디스크 위험 견종 (소시지형, 짧은 다리)
SPINAL_RISK_BREEDS = {
    "dachshund",
    "pembroke-welsh-corgi",
    "cardigan-welsh-corgi",
    "basset-hound",
    "skye-terrier",
}

# 슬개골 탈구 위험 (소형 견종 일반)
PATELLAR_RISK_SIZES = {"small"}


def compute_cost_estimate(
    breed_url_key: str,
    size: str,
    grooming_score: int | None,
    health_tests_count: int,
    life_expectancy_years: int | None = None,
) -> dict:
    """
    한국 시장 기준 월 양육비 추정 — '현재'와 '시니어' 두 단계로 분리.

    현재 비용 (입양 ~ 5세):
      - 사료, 그루밍, 용품, 돌발 의료비 (예방접종/구충/응급)

    시니어 비용 (7세 이상, 정기 노화 의료비):
      - 정기 검진, 관절 영양제, 만성질환 관리
      - 견종별 위험 (단두종/척추/슬개골/대형견 고관절) 가중치
    """

    # ─── 현재 비용 ───
    food = FOOD_COST_BY_SIZE.get(size, FOOD_COST_BY_SIZE["unknown"])

    g_score = grooming_score if grooming_score in (1, 2, 3, 4, 5) else 3
    grooming = GROOMING_COST[g_score].get(size, GROOMING_COST[g_score]["medium"])

    # 돌발 의료비: 기본 예방접종 + 구충 + 응급 대비
    size_med_factor = {"small": 1.0, "medium": 1.3, "large": 1.7, "giant": 2.2, "unknown": 1.3}
    medical_now = int(20_000 * size_med_factor.get(size, 1.3))  # 월 평균 (실제로는 분기·연 단위)

    supplies = 30_000

    current_low  = int((food + grooming + medical_now + supplies) * 0.85)
    current_high = int((food + grooming + medical_now + supplies) * 1.20)

    # 현재 비용 등급
    current_avg = (current_low + current_high) / 2
    if current_avg < 150_000:   current_level = "low"
    elif current_avg < 250_000: current_level = "medium"
    elif current_avg < 400_000: current_level = "high"
    else:                        current_level = "very_high"

    # ─── 시니어 비용 (7세 이상 노령기 정기 의료비) ───

    # 기본 정기 검진 + 영양제 (크기 기반)
    senior_base_by_size = {
        "small":   80_000,
        "medium": 120_000,
        "large":  180_000,
        "giant":  250_000,
        "unknown": 120_000,
    }
    senior_base = senior_base_by_size.get(size, 120_000)

    # 견종별 위험 가중치
    risk_factors = []
    risk_add = 0

    if breed_url_key in BRACHYCEPHALIC_BREEDS:
        risk_factors.append("단두종 (호흡기/안과 정기 관리)")
        risk_add += 60_000

    if breed_url_key in SPINAL_RISK_BREEDS:
        risk_factors.append("척추/디스크 위험")
        risk_add += 70_000

    if size in PATELLAR_RISK_SIZES:
        risk_factors.append("슬개골 탈구 위험 (소형견 일반)")
        risk_add += 25_000

    if size in ("large", "giant"):
        risk_factors.append("대형견 고관절·심장 노화")
        risk_add += 50_000

    if health_tests_count >= 5:
        risk_factors.append(f"견종 특이 건강검사 {health_tests_count}개")
        risk_add += health_tests_count * 8_000

    senior_low  = int((senior_base + risk_add) * 0.85)
    senior_high = int((senior_base + risk_add) * 1.30)

    senior_avg = (senior_low + senior_high) / 2
    if senior_avg < 150_000:   senior_level = "low"
    elif senior_avg < 250_000: senior_level = "medium"
    elif senior_avg < 400_000: senior_level = "high"
    else:                       senior_level = "very_high"

    level_kr_map = {"low": "낮음", "medium": "보통", "high": "높음", "very_high": "매우 높음"}

    return {
        # 현재 비용 (입양 직후 ~ 5세)
        "current": {
            "monthly_krw_min": current_low,
            "monthly_krw_max": current_high,
            "level":     current_level,
            "level_kr":  level_kr_map[current_level],
            "breakdown": {
                "food":         food,
                "grooming":     grooming,
                "medical":      medical_now,
                "supplies":     supplies,
            },
            "description": "사료·그루밍·용품·기본 의료비 (예방접종/구충/응급) 월평균",
        },
        # 시니어 비용 (7세 이후 정기 노화 의료비)
        "senior": {
            "monthly_krw_min": senior_low,
            "monthly_krw_max": senior_high,
            "level":     senior_level,
            "level_kr":  level_kr_map[senior_level],
            "risk_factors": risk_factors,
            "description": "노령기 정기 의료비 (검진·관절 영양제·만성질환 관리 등). 견종별 노화 위험 반영.",
        },
        # 메인 매칭에는 현재 비용 기준
        "level":            current_level,
        "level_kr":         level_kr_map[current_level],
        "monthly_krw_min":  current_low,
        "monthly_krw_max":  current_high,
        "factors": {
            "size":               size,
            "grooming_score":     g_score,
            "health_tests_count": health_tests_count,
            "breed_health_risks": risk_factors,
        },
    }


# ─── 3. 라이프스타일 태그 ──────────────────────────────────────

def compute_lifestyle_tags(
    traits: dict,
    size: str,
    coat_type: list,
    scores: dict,
    cost: dict,
) -> list[str]:
    """
    빠른 필터링용 불리언 태그 생성. 추천 알고리즘에서 손쉽게 활용.
    """
    tags = []

    # 크기 기반
    if size == "small":
        tags.append("small_dog")
    elif size in ("large", "giant"):
        tags.append("large_dog")

    # 털날림
    shed = scores.get("shedding", {}).get("raw")
    if shed is not None and shed <= 2:
        tags.append("low_shedding")
    if shed is not None and shed >= 4:
        tags.append("high_shedding")

    # 짖음
    bark = scores.get("barking", {}).get("raw")
    if bark is not None and bark <= 2:
        tags.append("quiet")
    if bark is not None and bark >= 4:
        tags.append("vocal")

    # 알러지 친화 (저알러지견)
    hypo_coats = {"hairless", "curly", "wavy", "corded"}
    if any(c.lower() in hypo_coats for c in (coat_type or [])):
        if shed is not None and shed <= 2:
            tags.append("hypoallergenic")

    # 아파트 친화
    energy = scores.get("exercise_needs", {}).get("raw_energy")
    if (
        size == "small"
        and (bark is None or bark <= 3)
        and (energy is None or energy <= 3)
    ):
        tags.append("apartment_friendly")

    # 초보자 친화
    train = scores.get("training_difficulty", {}).get("raw_trainability")
    friendly_avg = scores.get("friendliness", {}).get("avg_score", 0)
    if train is not None and train >= 4 and friendly_avg >= 3.5:
        tags.append("good_for_beginners")

    # 활동적/조용한 가정
    if energy is not None and energy <= 2:
        tags.append("low_energy")
    if energy is not None and energy >= 4:
        tags.append("high_energy")
        tags.append("needs_yard_or_long_walks")

    # 어린이 친화
    kids = scores.get("friendliness", {}).get("raw_with_children")
    if kids is not None and kids >= 4:
        tags.append("good_with_kids")

    # 다른 개와의 친화
    others = scores.get("friendliness", {}).get("raw_with_dogs")
    if others is not None and others >= 4:
        tags.append("good_with_other_dogs")

    # 비용 관련
    cost_level = cost.get("level")
    if cost_level == "low":
        tags.append("budget_friendly")
    if cost_level in ("high", "very_high"):
        tags.append("expensive_to_keep")

    # 훈련 강도
    diff = scores.get("training_difficulty", {}).get("difficulty_score")
    if diff is not None and diff >= 4:
        tags.append("requires_experienced_owner")

    return sorted(set(tags))


# ─── 4. 한국어 RAG chunks 생성 ────────────────────────────────

def compute_rag_chunks(
    breed_name: str,
    kr_name: str | None,
    breed_group: str | None,
    size: str,
    weight_display: str | None,
    height_display: str | None,
    life_expectancy: str | None,
    temperament: list[str],
    scores: dict,
    cost: dict,
    tags: list[str],
    kr_popularity_rank: int | None,
    kr_popularity_note: str | None,
    health_tests: list[str],
) -> list[dict]:
    """
    벡터 임베딩용 한국어 자연어 청크. 주제별로 분리해서 검색 정확도 향상.
    """
    name_kr = kr_name or breed_name
    chunks = []

    # ── intro ──
    rank_phrase = ""
    if kr_popularity_rank:
        if kr_popularity_rank <= 10:
            rank_phrase = f"한국에서 가장 인기 있는 견종 중 하나로 {kr_popularity_rank}위에 올라 있습니다. "
        elif kr_popularity_rank <= 30:
            rank_phrase = f"한국에서 꾸준히 사랑받는 견종으로 {kr_popularity_rank}위에 위치합니다. "
        else:
            rank_phrase = f"한국 인기 견종 50위 안에 드는 견종(현재 {kr_popularity_rank}위)입니다. "
    note = f"{kr_popularity_note} " if kr_popularity_note else ""
    intro_parts = [
        f"{name_kr}({breed_name})은(는) {SIZE_KR.get(size, '미상')} 견종입니다.",
        rank_phrase + note,
    ]
    if weight_display:
        intro_parts.append(f"체중은 {weight_display}, 키는 {height_display or '정보 없음'}입니다.")
    if life_expectancy:
        intro_parts.append(f"평균 수명은 {life_expectancy}입니다.")
    chunks.append({"topic": "intro", "topic_kr": "기본 소개", "text": " ".join(intro_parts)})

    # ── personality ──
    fr = scores.get("friendliness", {})
    pers_parts = []
    if temperament:
        pers_parts.append(f"기질 키워드: {', '.join(temperament[:8])}.")
    if fr:
        pers_parts.append(
            f"가족과의 친밀도는 {LEVEL_KR.get(LEVEL_BY_SCORE_5.get(fr.get('raw_with_family') or 3, 'medium'), '보통')}, "
            f"낯선 사람에 대한 개방성은 {LEVEL_KR.get(LEVEL_BY_SCORE_5.get(fr.get('raw_with_strangers') or 3, 'medium'), '보통')}, "
            f"다른 개와의 친화력은 {LEVEL_KR.get(LEVEL_BY_SCORE_5.get(fr.get('raw_with_dogs') or 3, 'medium'), '보통')} 수준입니다."
        )
        if fr.get("raw_with_children") and fr["raw_with_children"] >= 4:
            pers_parts.append("어린이와 잘 어울려 가족견으로 적합합니다.")
        elif fr.get("raw_with_children") and fr["raw_with_children"] <= 2:
            pers_parts.append("어린이와 함께 키울 때는 주의가 필요합니다.")
    if pers_parts:
        chunks.append({"topic": "personality", "topic_kr": "성격과 기질", "text": " ".join(pers_parts)})

    # ── shedding & grooming ──
    sh = scores.get("shedding", {})
    gr = scores.get("grooming", {})
    sg_parts = []
    if sh:
        if sh["raw"] <= 2:
            sg_parts.append(f"털날림이 적은 편({sh['level_kr']})이라 옷이나 가구에 털이 잘 묻지 않습니다.")
        elif sh["raw"] >= 4:
            sg_parts.append(f"털날림이 많은 편({sh['level_kr']})으로 정기적인 청소가 필요합니다.")
        else:
            sg_parts.append(f"털날림은 {sh['level_kr']} 수준입니다.")
    if gr:
        sg_parts.append(f"그루밍 빈도는 {gr.get('frequency_kr', '주 1회')} 권장({gr['level_kr']}).")
        if gr["raw"] >= 4:
            sg_parts.append("매일 빗질이 필요하며 정기적인 전문 미용이 권장됩니다.")
    if "hypoallergenic" in tags:
        sg_parts.append("저알러지 견종으로 알러지가 있는 분에게도 비교적 적합합니다.")
    if sg_parts:
        chunks.append({"topic": "shedding_grooming", "topic_kr": "털날림과 관리", "text": " ".join(sg_parts)})

    # ── barking ──
    ba = scores.get("barking", {})
    if ba:
        if ba["raw"] <= 2:
            text = f"짖음이 적은 편({ba['level_kr']})입니다. 아파트, 빌라 등 공동주택에 적합하며 이웃과의 갈등 가능성이 낮습니다."
        elif ba["raw"] >= 4:
            text = f"짖음이 많은 편({ba['level_kr']})입니다. 공동주택 거주 시 짖음 훈련이 필수적이며 이웃 간 소음 갈등에 주의해야 합니다."
        else:
            text = f"짖음은 {ba['level_kr']} 수준으로, 상황에 따라 적절히 짖는 편입니다."
        chunks.append({"topic": "barking", "topic_kr": "짖음 정도", "text": text})

    # ── training ──
    tr = scores.get("training_difficulty", {})
    if tr:
        text_parts = [
            f"훈련 난이도: {tr['level_kr']}. {tr.get('note', '')}"
        ]
        if tr["raw_trainability"] and tr["raw_trainability"] >= 4:
            text_parts.append(
                "학습 의욕이 강하고 보호자를 기쁘게 하려는 성향이 있어, 긍정 강화 훈련이 잘 통합니다. "
                "기본 훈련(앉아, 기다려, 배변 등)부터 차근차근 시작하면 좋은 유대감을 쌓을 수 있습니다."
            )
        elif tr["raw_trainability"] and tr["raw_trainability"] <= 2:
            text_parts.append(
                "독립심이 강하고 자기 주관이 뚜렷한 편이라 일관된 훈련과 인내가 필요합니다. "
                "초보 보호자보다는 경험자 또는 전문 훈련사의 도움을 받는 것을 권장합니다."
            )
        text_parts.append(
            "훈련을 잘 시키면 견종이 자신감과 안정감을 얻어 짖음·분리불안 등 문제 행동이 크게 줄어들고, "
            "보호자와의 신뢰 관계가 깊어집니다. 견종이 행복하면 가족 전체가 행복해집니다."
        )
        chunks.append({"topic": "training", "topic_kr": "훈련", "text": " ".join(text_parts)})

    # ── exercise ──
    ex = scores.get("exercise_needs", {})
    if ex:
        walk = ex.get("daily_walk_minutes", 45)
        text = (
            f"필요 운동량은 {ex['level_kr']} 수준이며, 권장 일일 산책 시간은 약 {walk}분입니다. "
        )
        if ex.get("raw_energy", 3) >= 4:
            text += "에너지가 매우 높은 견종으로, 산책 외에 뛰어놀 수 있는 공간이나 견종 스포츠가 필요합니다. 운동 부족 시 파괴 행동이 나타날 수 있습니다."
        elif ex.get("raw_energy", 3) <= 2:
            text += "활동량이 낮아 짧은 산책과 실내 놀이만으로도 충분합니다. 아파트 거주자에게 적합합니다."
        else:
            text += "적당한 산책과 놀이로 만족하는 편이라 대부분의 라이프스타일에 맞습니다."
        chunks.append({"topic": "exercise", "topic_kr": "운동량과 산책", "text": text})

    # ── cost in Korean context ──
    current = cost.get("current", {})
    senior = cost.get("senior", {})
    cur_min = current.get("monthly_krw_min", 0)
    cur_max = current.get("monthly_krw_max", 0)
    sen_min = senior.get("monthly_krw_min", 0)
    sen_max = senior.get("monthly_krw_max", 0)
    breakdown = current.get("breakdown", {})

    cost_text = (
        f"입양 초반(어린 시기) 월 양육비는 약 {cur_min:,}원 ~ {cur_max:,}원으로 추정됩니다 "
        f"({current.get('level_kr', '보통')} 수준). "
        f"구성: 사료 {breakdown.get('food', 0):,}원, 그루밍 {breakdown.get('grooming', 0):,}원, "
        f"기본 의료(예방접종/구충/응급) {breakdown.get('medical', 0):,}원, "
        f"용품 {breakdown.get('supplies', 0):,}원. "
    )
    cost_text += (
        f"7세 이후 시니어 시기에는 정기 의료비가 추가되어 월 약 {sen_min:,}원 ~ {sen_max:,}원으로 "
        f"증가할 수 있습니다 ({senior.get('level_kr', '보통')} 수준). "
    )
    risks = senior.get("risk_factors", [])
    if risks:
        cost_text += f"이 견종은 노령기에 {', '.join(risks)} 가능성이 있어 정기 검진과 관리가 중요합니다. "
    else:
        cost_text += "비교적 안정적인 노화 패턴을 보이는 견종입니다. "
    chunks.append({"topic": "cost_korea", "topic_kr": "한국 양육 비용 (현재 + 시니어)", "text": cost_text})

    # ── apartment & 한국 환경 fit ──
    apt_parts = []
    if "apartment_friendly" in tags:
        apt_parts.append("아파트, 빌라 등 공동주택에 적합한 견종입니다. 짖음이 적고 활동량도 무리하지 않아 도시 생활에 잘 적응합니다.")
    elif "needs_yard_or_long_walks" in tags:
        apt_parts.append("활동 욕구가 높아 공동주택보다는 마당이 있는 단독주택이나 장시간 산책이 가능한 환경에서 더 행복합니다.")
    if "good_for_beginners" in tags:
        apt_parts.append("초보 보호자에게도 추천할 만한 견종입니다.")
    if "requires_experienced_owner" in tags:
        apt_parts.append("훈련 경험이 있는 보호자에게 적합한 견종입니다.")
    if apt_parts:
        chunks.append({"topic": "korean_lifestyle_fit", "topic_kr": "한국 라이프스타일 적합도", "text": " ".join(apt_parts)})

    return chunks
