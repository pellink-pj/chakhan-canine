"""
AKC 크롤링 데이터 정리 스크립트

목적:
  1. popularity_2025 기준 100위 이내 견종만 남기기
  2. 각 견종 데이터를 하나의 객체로 깔끔하게 묶기 (중복 제거)
  3. temperament를 키워드 배열(리스트)로 변환
  4. traits의 기준 설명(점수 가이드)은 traits_guide.json으로 별도 분리
  5. popularity는 최근 5년(2021~2025)만 포함

결과 파일:
  - processed/breeds_top100.json : 100위 이내 견종 데이터
  - processed/traits_guide.json  : traits 점수 기준표 (1-5점 의미 설명)
"""

import json
import os

from breed_enrichment import (
    classify_size,
    compute_scores,
    compute_cost_estimate,
    compute_lifestyle_tags,
    compute_rag_chunks,
    lb_to_kg,
    inch_to_cm,
    build_size_display_kr,
    SIZE_KR,
)

# ─── 기본 설정 ───────────────────────────────────────────────
INPUT_DIR  = "/Users/yeonly/akc-crawler/result"   # 원본 JSON 파일 폴더
OUTPUT_DIR = "/Users/yeonly/akc-crawler/processed" # 결과 저장 폴더
POPULARITY_YEARS = list(range(2021, 2026))  # AKC popularity는 최근 5년만 포함 (참고용)

# ─── 한국 인기견종 매핑 ───────────────────────────────────────
# 출처: KB금융지주/농림축산식품부 통계 종합 (Gemini 정리)
# 형식: breed_name_url(AKC 키) → (한국 순위, 한국어 이름, 비고)
#
# 1~30위 = popular tier, 31~50위 = less_popular tier
# AKC에 없는 6개 견종(진돗개, 풍산개, 삽살개, 말티푸, 믹스견, 스피츠)은
# 데이터가 없어 제외. _meta.excluded_kr_breeds에 명시.
KR_POPULARITY = {

    "maltese":              (1,  "말티즈", "하얗고 조그만 우리 말티즈"),
    "poodle":           (2,  "푸들", "사랑받는 푸들, 토이 푸들, 미니어처 푸들! 스탠다드 푸들도 아셨나요?"),
    "mixed breed":     (2,  "믹스견", "비품종견, 잡종(雜種)이라고 하며 유머 섞인 말로 시그로자브종"),
    "pomeranian":           (4,  "포메라니안", ""),
    "korean-jindo-dog":     (5,  "진돗개", "마당이 있는 단독주택에서 인기있는 진돗개"),
    "shih-tzu":             (6,  "시츄", None),
    "bichon-frise":         (7,  "비숑 프리제", None),
    "chihuahua":            (8,  "치와와", None),
    "golden-retriever":     (9,  "골든 리트리버", None),
    "yorkshire-terrier":    (10, "요크셔 테리어", None),

    # 11~30위: 인기 소·중형견 및 최근 트렌드
    "japanese-spitz":       (11, "스피츠 (일본)", "한국에서 흔히 '스피츠'로 불리는 작고 흰 견종"),
    "pembroke-welsh-corgi": (12, "펨브로크 웰시 코기", None),
    "cardigan-welsh-corgi": (12, "카디건 웰시 코기", None),
    "dachshund":            (13, "닥스훈트", None),
    # 14위 Maltipoo: AKC 데이터 없음 (하이브리드)
    "beagle":               (15, "비글", None),
    "french-bulldog":       (16, "프렌치 불독", None),
    "border-collie":        (17, "보더 콜리", None),
    "shiba-inu":            (18, "시바견", None),
    "pekingese":            (19, "페키니즈", None),
    "miniature-schnauzer":  (20, "미니어처 슈나우저", None),
    "cocker-spaniel":       (21, "코카 스파니엘", None),
    "labrador-retriever":   (22, "래브라도 리트리버", None),
    "coton-de-tulear":      (23, "꼬통 드 툴레아", "특유의 외모로 최근 인기 급부상"),
    "italian-greyhound":    (24, "이탈리안 그레이하운드", None),
    "pug":                  (25, "퍼그", None),
    "boston-terrier":       (26, "보스턴 테리어", None),
    "samoyed":              (27, "사모예드", None),
    "papillon":             (28, "파피용", None),
    "cavalier-king-charles-spaniel": (29, "카발리에 킹 찰스 스파니엘", None),
    "siberian-husky":       (30, "시베리안 허스키", None),

    # 31~50위: 마니아층/특수·대형 견종
    "bedlington-terrier":   (31, "베들링턴 테리어", None),
    "alaskan-malamute":     (32, "알래스칸 말라뮤트", None),
    "chow-chow":            (33, "차우차우", None),
    "dalmatian":            (34, "달마시안", None),
    "russell-terrier":      (35, "잭 러셀 테리어", None),
    "doberman-pinscher":    (36, "도베르만 핀셔", None),
    "german-shepherd-dog":  (37, "저먼 셰퍼드", None),
    "great-pyrenees":       (38, "그레이트 피레니즈", None),
    "rottweiler":           (39, "로트와일러", None),
    "shetland-sheepdog":    (40, "셔틀랜드 쉽독", None),
    "bull-terrier":         (41, "불테리어", None),
    "bulldog":              (42, "잉글리쉬 불독", None),
    # 43위 Pungsan Dog, 44위 Sapsali: AKC 데이터 없음
    "afghan-hound":         (45, "아프간 하운드", None),
    "greyhound":            (46, "그레이하운드", None),
    "saint-bernard":        (47, "세인트 버나드", None),
    "collie":               (48, "콜리", None),
    "belgian-malinois":     (49, "벨지안 말리노이즈", None),
    "borzoi":               (50, "보르조이", None),
}

# 한국 50위 밖이지만 해외에서 인기 있는 견종들 한국어 이름
# (멍메이트 "해외 히든 젬" 카테고리)
INTL_KR_NAMES = {
    "poodle-standard":              "스탠다드 푸들",
    "australian-shepherd":          "오스트레일리안 셰퍼드",
    "bernese-mountain-dog":         "버니즈 마운틴 도그",
    "cane-corso":                   "케인 코르소",
    "boxer":                        "복서",
    "great-dane":                   "그레이트 데인",
    "havanese":                     "하바니즈",
    "english-springer-spaniel":     "잉글리시 스프링거 스파니엘",
    "miniature-american-shepherd":  "미니어처 아메리칸 셰퍼드",
    "german-shorthaired-pointer":   "저먼 쇼트헤어드 포인터",
}

# ─── 견종 페이지 콘텐츠 (intro + caution) ────────────────────────────────
# 견종 페이지 들어왔을 때 보이는 짧은 매력 설명 + "앗, 하지만" 박스 내용.
# 톤: 친근(첫인상) → 진지(주의사항). 멍메이트 시그니처 톤.
#
# 입력 형식:
#   "breed-slug": {
#       "intro": "짧은 매력 설명 (1~3문장). 견종 페이지 인삿말.",
#       "caution": "앗, 하지만 박스 내용 (1~3문장). 키우기 전 알아야 할 거.",
#   },
#
# Co가 견본 1개 박으면 → 그 톤으로 나머지 한국 인기 50견종 1차 박음 → Co 검수.

BREED_CONTENT = {
    # ─── 견본 (Co가 박는 자리) ───
    "poodle-toy": {
        "intro": "털이 날리지 않아요. 똑똑해서 훈련이 쉬워요.",
        "caution": "여기에 앗, 하지만 피부병 예방을 위해 빗질 (매일 필수)",
    },
    "pomeranian": {
        "intro": "뽀송뽀송 귀여운 당당한 애교쟁이",
        "caution": "여기에 앗, 질투가 많아서 훈련 필수",
    },

    # 나머지 견종은 Co 견본 받은 후 같은 톤으로 박을 자리
}


# AKC에 없는 한국 인기견종 (메타에 기록용)
EXCLUDED_KR_BREEDS = [
    {"kr_rank": 3,  "name": "Mixed Breed",  "kr_name": "믹스견",     "reason": "AKC 견종 등록 없음 (믹스)"},
    {"kr_rank": 14, "name": "Maltipoo",     "kr_name": "말티푸",     "reason": "AKC 미등록 (하이브리드)"},
    {"kr_rank": 43, "name": "Pungsan Dog",  "kr_name": "풍산개",     "reason": "AKC 미등록 (한국 토종)"},
    {"kr_rank": 44, "name": "Sapsali",      "kr_name": "삽살개",     "reason": "AKC 미등록 (한국 토종)"},
]

# 변종 그룹 매핑 (Poodle Toy/Mini/Standard, Welsh Corgi Pembroke/Cardigan)
VARIETY_GROUPS = {
    "poodle-toy":           ("poodle", "Toy"),
    "poodle-miniature":     ("poodle", "Miniature"),
    "poodle-standard":      ("poodle", "Standard"),
    "pembroke-welsh-corgi": ("welsh-corgi", "Pembroke"),
    "cardigan-welsh-corgi": ("welsh-corgi", "Cardigan"),
}


def compute_kr_tier(kr_rank: int | None) -> str:
    """
    한국 인기 순위를 3-tier로 분류.
      - popular:      1~30위  (흔히 보는 견종, 무난한 선택)
      - less_popular: 31~50위 (알려졌지만 매니아층, 대형/특수견 위주)
      - unique:       그 외   (한국에서 거의 안 키우는 견종)
    """
    if kr_rank is None:
        return "unique"
    if kr_rank <= 30:
        return "popular"
    if kr_rank <= 50:
        return "less_popular"
    return "unique"


os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── 헬퍼 함수 ───────────────────────────────────────────────

def parse_temperament(raw: str) -> list[str]:
    """
    "playful / affectionate / calm" 형식의 문자열을
    ["playful", "affectionate", "calm"] 리스트로 변환
    """
    if not raw:
        return []
    return [t.strip() for t in raw.split("/") if t.strip()]


def extract_breed_data(raw: dict) -> dict | None:
    """
    원본 JSON에서 필요한 데이터만 꺼내서 깔끔하게 정리.
    popularity_2025가 30위 초과면 None 반환 (버림).
    """
    try:
        breed_data = raw["settings"]["breed_data"]

        # ── basics (기본 정보) ──
        basics_section = breed_data["basics"]
        breed_key = list(basics_section.keys())[0]  # ex: "whippet"
        basics = basics_section[breed_key]

        breed_url_key = basics.get("breed_name_url", "")

        # ── AKC 순위 (참고용) ──
        # 2025 → 2024 → ... 순으로 가장 최근 유효 연도 사용
        akc_rank = None
        akc_rank_year = None
        for year in (2025, 2024, 2023, 2022, 2021):
            v = basics.get(f"popularity_{year}")
            if v is not None:
                akc_rank = v
                akc_rank_year = year
                break

        # ── 한국 인기 (메인) ──
        kr_info = KR_POPULARITY.get(breed_url_key)
        if kr_info is not None:
            kr_rank, kr_name, kr_note = kr_info
        else:
            kr_rank, kr_name, kr_note = None, None, None
            # 해외 인기 견종도 한국어 이름 박기 (히든 젬 카테고리)
            kr_name = INTL_KR_NAMES.get(breed_url_key)

        kr_tier = compute_kr_tier(kr_rank)

        # 변종 그룹 정보
        variety_group, variety = VARIETY_GROUPS.get(breed_url_key, (None, None))

        # ── traits (특성 점수) ──
        traits_section = breed_data.get("traits", {})
        traits_raw = traits_section.get(breed_key, {}).get("traits", {})
        temperament_raw = traits_section.get(breed_key, {}).get("temperament", "")

        # traits에서 score만 추출 (설명은 traits_guide.json에 따로 저장)
        traits_scores = {}
        for trait_key, trait_val in traits_raw.items():
            if isinstance(trait_val, dict):
                score = trait_val.get("score")
                selected = trait_val.get("selected")  # checkbox형 항목 (coat_type 등)
                if selected is not None and isinstance(selected, list) and len(selected) > 0:
                    # checkbox형: 선택된 값 리스트로 저장
                    traits_scores[trait_key] = selected
                elif score is not None and score != 0:
                    # radio형: 점수 저장
                    traits_scores[trait_key] = score
                elif score == 0 and selected and len(selected) > 0:
                    traits_scores[trait_key] = selected

        # ── description (설명문) ──
        desc_section = breed_data.get("description", {})
        desc = desc_section.get(breed_key, {})

        # ── standards (체형 기준) ──
        standards_section = breed_data.get("standards", {})
        standards = standards_section.get(breed_key, {})

        # ── health (건강 정보) ──
        health_section = breed_data.get("health", {})
        health = health_section.get(breed_key, {})

        # ── history (역사) ──
        history_section = breed_data.get("history", {})
        history = history_section.get(breed_key, {})

        # ── colors (털 색상) ──
        colors_section = breed_data.get("colors", {})
        colors_raw = colors_section.get(breed_key, {}).get("colors", [])
        # Standard(S)와 Alternate(A) 색상 분리
        colors_standard  = [c["color_long"] for c in colors_raw if c.get("standard_alternate") == "S"]
        colors_alternate = [c["color_long"] for c in colors_raw if c.get("standard_alternate") == "A"]

        # ── markings (무늬) ──
        markings_section = breed_data.get("markings", {})
        markings_raw = markings_section.get(breed_key, {}).get("markings", [])
        markings_standard  = [m["markings_long"] for m in markings_raw if m.get("standard_alternate") == "S"]
        markings_alternate = [m["markings_long"] for m in markings_raw if m.get("standard_alternate") == "A"]

        # ── clubs (클럽/구조 연락처) ──
        clubs_section = breed_data.get("clubs", {})
        clubs = clubs_section.get(breed_key, {})

        # ── breed 미디어 (갤러리 이미지) ──
        media = raw.get("breed", {}).get("media", {})
        gallery = [img["src"] for img in media.get("gallery", []) if img.get("src")]
        standard_img = media.get("standard", {}).get("src", "")

        # ── 건강 검사 목록 ──
        health_tests = []
        for i in range(1, 10):
            t = health.get(f"test_{i}", "")
            if t:
                health_tests.append(t)

        # ─── enrichment: scores / cost / tags / rag_chunks ───
        coat_type_list = traits_scores.get("coat_type", []) if isinstance(traits_scores.get("coat_type"), list) else []
        size_cat = classify_size(standards.get("weight_min"), standards.get("weight_max"))

        scores = compute_scores(traits_scores)

        cost_estimate = compute_cost_estimate(
            breed_url_key=basics.get("breed_name_url", ""),
            size=size_cat,
            grooming_score=scores.get("grooming", {}).get("raw"),
            health_tests_count=len(health_tests),
        )

        lifestyle_tags = compute_lifestyle_tags(
            traits=traits_scores,
            size=size_cat,
            coat_type=coat_type_list,
            scores=scores,
            cost=cost_estimate,
        )

        rag_chunks = compute_rag_chunks(
            breed_name=basics["breed_name"],
            kr_name=kr_name,
            breed_group=basics.get("breed_group"),
            size=size_cat,
            weight_display=standards.get("weight_display"),
            height_display=standards.get("height_display"),
            life_expectancy=basics.get("life_expectancy"),
            temperament=parse_temperament(temperament_raw),
            scores=scores,
            cost=cost_estimate,
            tags=lifestyle_tags,
            kr_popularity_rank=kr_rank,
            kr_popularity_note=kr_note,
            health_tests=health_tests,
        )

        # ─── 최종 결과 객체 조립 ───
        result = {
            # MongoDB _id 용 (breed_name_url을 그대로 사용 — 견종 변종도 unique)
            "_id":               basics["breed_name_url"],

            # 기본 식별 정보
            "breed_name":        basics["breed_name"],
            "breed_name_url":    basics["breed_name_url"],
            "akc_code":          basics.get("akc_code"),
            "origin":            basics.get("origin"),
            "breed_group":       basics.get("breed_group"),
            "year_recognized":   basics.get("year_recognized"),
            "life_expectancy":   basics.get("life_expectancy"),

            # ── 한국 기준 (메인) ──
            "kr_name":             kr_name,           # 한국어 견종명
            "kr_popularity_rank":  kr_rank,           # 한국 순위 (1~50, 없으면 null)
            "kr_popularity_tier":  kr_tier,           # popular | less_popular | unique
            "kr_popularity_note":  kr_note,           # 인기 이유/특징 (있으면)

            # ── AKC 기준 (참고용 — 외국 인기견종 추천 시 활용) ──
            "akc_popularity_rank":      akc_rank,
            "akc_popularity_rank_year": akc_rank_year,
            "akc_popularity_history": {
                str(year): basics.get(f"popularity_{year}")
                for year in POPULARITY_YEARS
                if basics.get(f"popularity_{year}") is not None
            },

            # 변종 그룹 (같은 group_key는 추천 시 묶어서 dedupe 가능)
            "variety_group": variety_group,
            "variety": variety,

            # ════════════════════════════════════════════════════
            # 추천 시스템용 enrichment 필드들
            # ════════════════════════════════════════════════════

            # 크기 카테고리 (small/medium/large/giant)
            "size_category":    size_cat,
            "size_category_kr": SIZE_KR.get(size_cat),

            # 핵심 점수 카테고리 (사용자 매칭용)
            # - shedding(털날림), barking(짖음), grooming(그루밍)
            # - exercise_needs(운동량), training_difficulty(훈련강도)
            # - friendliness(친화력)
            "scores": scores,

            # 한국 시장 기준 월 양육비 추정
            # 식비 + 그루밍 + 의료비 + 용품 + 훈련/케어
            "cost_estimate": cost_estimate,

            # 추천 알고리즘 필터용 불리언 태그
            "lifestyle_tags": lifestyle_tags,

            # RAG 벡터 임베딩용 한국어 자연어 청크
            "rag_chunks": rag_chunks,

            # 기질 키워드 (메타데이터처럼)
            "temperament": parse_temperament(temperament_raw),

            # 특성 점수 (1-5점 기준은 traits_guide.json 참고)
            "traits": traits_scores,

            # ─── 체형 (한국 단위 메인, AKC 원본은 raw_akc에 보존) ───
            "weight_kg_min":      lb_to_kg(standards.get("weight_min")),
            "weight_kg_max":      lb_to_kg(standards.get("weight_max")),
            "height_cm_min_male": inch_to_cm(standards.get("height_min_m")),
            "height_cm_max_male": inch_to_cm(standards.get("height_max_m")),
            "height_cm_min_female": inch_to_cm(standards.get("height_min_f")),
            "height_cm_max_female": inch_to_cm(standards.get("height_max_f")),
            # 사용자에게 바로 보여줄 수 있는 한국어 표현
            **build_size_display_kr(
                lb_to_kg(standards.get("weight_min")),
                lb_to_kg(standards.get("weight_max")),
                inch_to_cm(standards.get("height_min_m")),
                inch_to_cm(standards.get("height_max_m")),
                inch_to_cm(standards.get("height_min_f")),
                inch_to_cm(standards.get("height_max_f")),
            ),

            # 외형 (사용자가 색상 검색 등에 활용)
            "colors": {
                "standard":  colors_standard,
                "alternate": colors_alternate
            },
            "markings": {
                "standard":  markings_standard,
                "alternate": markings_alternate
            },

            # 건강 검사 (의료비 추정에도 사용)
            "health_tests": health_tests,

            # 이미지
            "images": {
                "standard": standard_img,
                "gallery":  gallery
            },
        }

        # None인 필드 제거 (깔끔하게)
        result = {k: v for k, v in result.items() if v is not None and v != "" and v != [] and v != {}}

        # ─── 별도 article (게시판 콘텐츠용) ───
        article = {
            "_id": basics["breed_name_url"],
            "breed_name": basics["breed_name"],
            "kr_name":    kr_name,
            "blurb":          desc.get("akc_org_blurb"),
            "about":          desc.get("akc_org_about"),
            "description":    desc.get("mp_description"),
            "health_info":    health.get("akc_org_health"),
            "nutrition_info": health.get("akc_org_nutrition"),
            "grooming_info":  health.get("akc_org_grooming"),
            "exercise_info":  health.get("akc_org_exercise"),
            "training_info":  health.get("akc_org_training"),
            "history":        history.get("akc_org_history"),
            "history_job":    history.get("mp_history_job"),
            "did_you_know": [fact.strip() for fact in history.get("did_you_know", "").split("|") if fact.strip()],
        }
        article = {k: v for k, v in article.items() if v is not None and v != "" and v != []}

        return result, article

    except Exception as e:
        print(f"  ⚠ 파싱 오류: {e}")
        return None, None


def extract_traits_guide(raw: dict) -> dict:
    """
    traits의 설명/기준 텍스트를 한 번만 추출해서 가이드 파일로 만들기.
    어떤 견종 JSON이든 이 구조는 동일하므로 첫 번째 파일에서 추출.
    """
    try:
        breed_data = raw["settings"]["breed_data"]
        traits_section = breed_data.get("traits", {})
        breed_key = list(traits_section.keys())[0]
        traits_raw = traits_section[breed_key].get("traits", {})

        guide = {}
        for trait_key, trait_val in traits_raw.items():
            if not isinstance(trait_val, dict):
                continue

            trait_type = trait_val.get("type", "radio")

            if trait_type == "radio":
                guide[trait_key] = {
                    "name":         trait_val.get("traits"),
                    "group":        trait_val.get("breed_group"),
                    "description":  trait_val.get("description"),
                    "scale": {
                        "1": trait_val.get("low_value_1"),
                        "3": trait_val.get("middle_value_3"),
                        "5": trait_val.get("high_value_5")
                    }
                }
            elif trait_type == "checkbox":
                choices = trait_val.get("choices", [])
                guide[trait_key] = {
                    "name":        trait_val.get("traits"),
                    "group":       trait_val.get("breed_group"),
                    "description": trait_val.get("description"),
                    "type":        "checkbox",
                    "choices":     choices if isinstance(choices, list) else []
                }

        return guide
    except Exception as e:
        print(f"  ⚠ 가이드 추출 오류: {e}")
        return {}


# ─── 메인 실행 ───────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  AKC 견종 데이터 정리 (한국 인기 기준 재설계)")
    print("  - 모든 AKC 견종 포함, kr_popularity_tier로 분류")
    print("  - popular(1~30) | less_popular(31~50) | unique(그 외)")
    print("=" * 60)

    json_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".json")]
    print(f"\n📂 총 {len(json_files)}개 JSON 파일 발견\n")

    all_breeds = []
    all_articles = []
    traits_guide = None
    failed = 0

    for fname in sorted(json_files):
        fpath = os.path.join(INPUT_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            print(f"  ✗ 읽기 실패: {fname} ({e})")
            failed += 1
            continue

        # traits 가이드는 처음 한 번만 추출
        if traits_guide is None:
            guide_candidate = extract_traits_guide(raw)
            if guide_candidate:
                traits_guide = guide_candidate

        # 견종 데이터 정리 — (breed, article) 튜플 반환
        breed, article = extract_breed_data(raw)
        if breed is None:
            failed += 1
            continue

        all_breeds.append(breed)
        if article:
            all_articles.append(article)

    # ── 정렬: kr_rank 우선, 없으면 akc_rank, 그 외는 이름순 ──
    def sort_key(b):
        kr = b.get("kr_popularity_rank")
        akc = b.get("akc_popularity_rank")
        # 1순위: 한국 순위 있는 견종 (오름차순)
        # 2순위: AKC 순위 있는 견종 (오름차순)
        # 3순위: 알파벳순
        return (
            kr is None,
            kr if kr is not None else 999,
            akc is None,
            akc if akc is not None else 999,
            b.get("breed_name", "")
        )
    all_breeds.sort(key=sort_key)

    # ── 출력: 정렬 후 견종 목록 표시 ──
    from collections import Counter
    tier_counts = Counter(b.get("kr_popularity_tier") for b in all_breeds)
    for b in all_breeds:
        kr_rank = b.get("kr_popularity_rank")
        kr_name = b.get("kr_name")
        tier = b.get("kr_popularity_tier")
        akc_rank = b.get("akc_popularity_rank")

        if kr_rank is not None:
            label = f"한국 {kr_rank}위 · {tier}"
            if kr_name:
                label += f" · {kr_name}"
        else:
            akc_label = f"AKC {akc_rank}위" if akc_rank else "AKC 미상"
            label = f"{tier} ({akc_label})"
        print(f"  ✓ {b['breed_name']:<38} {label}")

    # ── breeds_top100.json 저장 ──
    breeds_output = {
        "_meta": {
            "description": (
                "AKC 크롤링 견종 데이터를 한국 인기 순위 기준으로 재분류. "
                "모든 AKC 견종을 포함하고 kr_popularity_tier(popular/less_popular/unique)로 추천 분류."
            ),
            "source_kr_popularity": "KB금융지주/농림축산식품부 통계 종합 (Gemini 정리, 1~50위)",
            "total_breeds":  len(all_breeds),
            "tier_counts":   dict(tier_counts),
            "traits_guide_file": "traits_guide.json",
            "kr_popularity_tier_meaning": {
                "popular":      "인기 — 한국 1~30위. 흔히 보는 견종, 무난한 선택 (소형견 위주)",
                "less_popular": "비인기 — 한국 31~50위. 알려진 견종이지만 매니아층 (대형/특수견 위주)",
                "unique":       "유닉 — 한국 50위 밖. 잘 안 키우는 견종 (외국에서만 인기인 경우 등)"
            },
            "excluded_kr_breeds": EXCLUDED_KR_BREEDS,
            "fields_note": (
                "kr_popularity_rank=한국 순위(1~50, 없으면 null). "
                "kr_popularity_tier=추천 분류. "
                "kr_name=한국어 견종명. "
                "akc_popularity_rank=AKC 미국 순위(참고용). "
                "akc_popularity_history=연도별 AKC 순위. "
                "variety_group=같은 견종의 변종 묶음 키(예: poodle, welsh-corgi). "
                "variety=변종 이름(Toy/Miniature/Standard, Pembroke/Cardigan 등)."
            )
        },
        "breeds": all_breeds
    }

    breeds_path = os.path.join(OUTPUT_DIR, "breeds.json")
    with open(breeds_path, "w", encoding="utf-8") as f:
        json.dump(breeds_output, f, ensure_ascii=False, indent=2)

    # ── MongoDB import용 NDJSON (한 견종 = 한 줄) ──
    # 사용법: mongoimport --db dog_recommender --collection breeds --file breeds.ndjson
    ndjson_path = os.path.join(OUTPUT_DIR, "breeds.ndjson")
    with open(ndjson_path, "w", encoding="utf-8") as f:
        for breed in all_breeds:
            f.write(json.dumps(breed, ensure_ascii=False) + "\n")

    # ── breed_articles.json: 게시판 콘텐츠용 영어 원문 ──
    # 추천에는 쓰지 않지만 "이 견종 더 알아보기" 게시판/상세 페이지에 활용
    articles_output = {
        "_meta": {
            "description": "견종별 영어 상세 콘텐츠 (게시판/상세페이지용). 추천 시스템에는 사용하지 않음.",
            "fields": "blurb/about/description=AKC 견종 소개. health/nutrition/grooming/exercise/training_info=AKC 케어 가이드. history/history_job=역사와 본래 역할. did_you_know=재미있는 사실 리스트.",
            "total_breeds": len(all_articles),
            "note": "한국어 번역이 필요하면 별도 LLM 후처리 권장."
        },
        "articles": all_articles
    }
    articles_path = os.path.join(OUTPUT_DIR, "breed_articles.json")
    with open(articles_path, "w", encoding="utf-8") as f:
        json.dump(articles_output, f, ensure_ascii=False, indent=2)

    articles_ndjson_path = os.path.join(OUTPUT_DIR, "breed_articles.ndjson")
    with open(articles_ndjson_path, "w", encoding="utf-8") as f:
        for art in all_articles:
            f.write(json.dumps(art, ensure_ascii=False) + "\n")

    # ── traits_guide.json 저장 ──
    if traits_guide:
        guide_output = {
            "_meta": {
                "description": "AKC 견종 traits(특성) 점수 기준표. 모든 견종에 공통 적용됨.",
                "scale_explanation": "radio형 항목은 1-5점. 1=low_value, 3=middle_value, 5=high_value. checkbox형은 여러 값 선택 가능."
            },
            "traits": traits_guide
        }
        guide_path = os.path.join(OUTPUT_DIR, "traits_guide.json")
        with open(guide_path, "w", encoding="utf-8") as f:
            json.dump(guide_output, f, ensure_ascii=False, indent=2)
    
    # ── 결과 요약 ──
    print("\n" + "=" * 55)
    print(f"  ✅ 완료!")
    print(f"  - 포함된 견종: {len(all_breeds)}개")
    print(f"  - 처리 실패:   {failed}개")
    print(f"\n  Tier 분포:")
    for tier, cnt in sorted(tier_counts.items(), key=lambda x: ['popular','less_popular','unique'].index(x[0])):
        print(f"    {tier:<14}: {cnt}개")
    print(f"\n  ⚠ AKC에 없는 한국 인기견종 {len(EXCLUDED_KR_BREEDS)}개는 제외됨 (_meta.excluded_kr_breeds 참고):")
    for ex in EXCLUDED_KR_BREEDS:
        print(f"    - {ex['kr_name']} (한국 {ex['kr_rank']}위) — {ex['reason']}")
    print(f"\n  저장 위치:")
    print(f"  📄 {breeds_path}              (메인 데이터)")
    print(f"  📄 {ndjson_path}            (MongoDB import용)")
    print(f"  📄 {articles_path}        (게시판 콘텐츠)")
    print(f"  📄 {articles_ndjson_path}      (게시판 NDJSON)")
    if traits_guide:
        print(f"  📄 {guide_path}        (traits 점수 1~5 기준)")
    print("=" * 60)


if __name__ == "__main__":
    main()
