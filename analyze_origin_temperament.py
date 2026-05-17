"""
원산지(Origin)와 성격(Temperament) 연관성 분석 스크립트

사용 방법:
  1. 먼저 process_data.py를 실행해서 breeds_top100.json을 만들어야 합니다.
  2. 그 다음 이 스크립트를 실행하세요.

출력:
  - 콘솔에 분석 결과 출력
  - processed/origin_temperament_analysis.json 저장
"""

import json
import os
from collections import defaultdict, Counter

# ─── 설정 ───────────────────────────────────────────────
INPUT_FILE = "/Users/yeonly/akc-crawler/processed/breeds_top100.json"
OUTPUT_FILE = "/Users/yeonly/akc-crawler/processed/origin_temperament_analysis.json"

# ─── 원산지 → 지역 그룹 매핑 ───────────────────────────
# 비슷한 나라/지역을 큰 그룹으로 묶어서 분석
ORIGIN_TO_REGION = {
    # 영국/아일랜드
    "England": "영국/아일랜드",
    "Scotland": "영국/아일랜드",
    "Wales": "영국/아일랜드",
    "Ireland": "영국/아일랜드",
    "Great Britain": "영국/아일랜드",
    "United Kingdom": "영국/아일랜드",

    # 독일/오스트리아/스위스 (독어권)
    "Germany": "독일권",
    "Austria": "독일권",
    "Switzerland": "독일권",

    # 프랑스/벨기에 (프랑스권)
    "France": "프랑스/벨기에",
    "Belgium": "프랑스/벨기에",

    # 미국/캐나다 (북미)
    "United States": "북미",
    "Canada": "북미",

    # 일본/한국/중국 (동아시아)
    "Japan": "동아시아",
    "China": "동아시아",
    "Korea": "동아시아",

    # 북유럽 (스칸디나비아)
    "Norway": "북유럽",
    "Sweden": "북유럽",
    "Finland": "북유럽",
    "Iceland": "북유럽",
    "Denmark": "북유럽",

    # 러시아/동유럽
    "Russia": "러시아/동유럽",
    "Poland": "러시아/동유럽",
    "Hungary": "러시아/동유럽",
    "Czech Republic": "러시아/동유럽",

    # 남유럽 (이탈리아/스페인/포르투갈)
    "Italy": "남유럽",
    "Spain": "남유럽",
    "Portugal": "남유럽",
    "Malta": "남유럽",

    # 중동/아프리카
    "Egypt": "중동/아프리카",
    "Africa": "중동/아프리카",
    "Sahel Region": "중동/아프리카",

    # 중앙아시아/티베트
    "Tibet": "중앙아시아/티베트",
    "China/Tibet": "중앙아시아/티베트",

    # 호주
    "Australia": "호주",
}

def get_region(origin: str) -> str:
    """원산지 문자열에서 지역 그룹을 반환."""
    if not origin:
        return "불명"

    # 정확히 일치하는 게 있으면 바로 반환
    if origin in ORIGIN_TO_REGION:
        return ORIGIN_TO_REGION[origin]

    # 부분 일치로 찾기 (ex: "England, United Kingdom" 같은 경우)
    for key, region in ORIGIN_TO_REGION.items():
        if key.lower() in origin.lower():
            return region

    # 매핑에 없으면 원래 값 그대로 "기타"로 표시
    return f"기타({origin})"


def analyze():
    # ─── 파일 로드 ───────────────────────────────────────
    if not os.path.exists(INPUT_FILE):
        print("❌ breeds_top100.json 파일이 없습니다!")
        print("   먼저 process_data.py를 실행해 주세요.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    breeds = data["breeds"]
    print(f"\n📊 분석 대상: {len(breeds)}개 견종 (2025년 기준 상위 100위)\n")

    # ─── 데이터 수집 ─────────────────────────────────────
    # 지역별로 temperament 키워드 모으기
    region_keywords = defaultdict(list)      # region → [keyword, ...]
    region_breeds   = defaultdict(list)      # region → [breed_name, ...]
    origin_map      = {}                     # breed_name → (origin, region)

    for breed in breeds:
        name   = breed.get("breed_name", "?")
        origin = breed.get("origin", "")
        temps  = breed.get("temperament", [])
        region = get_region(origin)

        origin_map[name] = (origin, region)
        region_breeds[region].append(name)

        for kw in temps:
            kw_clean = kw.strip().lower()
            if kw_clean:
                region_keywords[region].append(kw_clean)

    # ─── 지역별 분석 ─────────────────────────────────────
    print("=" * 65)
    print("  📍 원산지(지역) 별 대표 성격 키워드 분석")
    print("=" * 65)

    region_analysis = {}

    # 견종 수 많은 순서로 정렬
    sorted_regions = sorted(region_breeds.keys(),
                            key=lambda r: len(region_breeds[r]),
                            reverse=True)

    for region in sorted_regions:
        breed_list = region_breeds[region]
        keywords   = region_keywords[region]

        if not keywords:
            continue

        # 키워드 빈도 계산
        kw_counter = Counter(keywords)
        top_keywords = kw_counter.most_common(8)  # 상위 8개

        print(f"\n🌍 {region} ({len(breed_list)}종)")
        print(f"   견종: {', '.join(breed_list)}")
        print(f"   대표 성격: ", end="")
        print(" | ".join(f"{kw}({cnt})" for kw, cnt in top_keywords))

        region_analysis[region] = {
            "breed_count": len(breed_list),
            "breeds": breed_list,
            "top_keywords": [
                {"keyword": kw, "count": cnt}
                for kw, cnt in top_keywords
            ],
            "all_keywords": dict(kw_counter)
        }

    # ─── 전체 TOP 키워드 ─────────────────────────────────
    print("\n" + "=" * 65)
    print("  🏆 전체 상위 100위 견종 공통 성격 키워드 TOP 20")
    print("=" * 65)

    all_keywords = []
    for kws in region_keywords.values():
        all_keywords.extend(kws)

    total_counter = Counter(all_keywords)
    print()
    for rank, (kw, cnt) in enumerate(total_counter.most_common(20), 1):
        bar = "█" * cnt
        print(f"  {rank:2}. {kw:<25} {cnt:3}회  {bar}")

    # ─── 지역별 고유 성격 (다른 지역에서 잘 안나오는 키워드) ───
    print("\n" + "=" * 65)
    print("  ✨ 지역별 '특징적인' 성격 (해당 지역에서만 두드러지는 키워드)")
    print("=" * 65)

    distinctive = {}
    for region in sorted_regions:
        if region not in region_keywords or len(region_breeds[region]) < 2:
            continue

        my_kws    = Counter(region_keywords[region])
        other_kws = Counter()
        for r2, kws in region_keywords.items():
            if r2 != region:
                other_kws.update(kws)

        # 이 지역에서 비율이 높고, 다른 지역 대비 상대적으로 더 많이 나오는 키워드
        unique_scores = {}
        for kw, my_cnt in my_kws.items():
            other_cnt = other_kws.get(kw, 0)
            my_ratio  = my_cnt / max(len(region_keywords[region]), 1)
            # 다른 지역 전체 대비 비율
            other_ratio = other_cnt / max(len(all_keywords) - len(region_keywords[region]), 1)
            # 상대 점수: 내 비율 / 전체 비율 (높을수록 이 지역 특징적)
            score = my_ratio / max(other_ratio, 0.001)
            if my_cnt >= 2:  # 최소 2번 이상 등장한 것만
                unique_scores[kw] = round(score, 2)

        top_unique = sorted(unique_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        if top_unique:
            print(f"\n🎯 {region}")
            for kw, score in top_unique:
                print(f"   - {kw:<25} (특징도: {score:.1f}x)")
            distinctive[region] = [{"keyword": kw, "score": score} for kw, score in top_unique]

    # ─── 결과 저장 ───────────────────────────────────────
    output = {
        "_meta": {
            "description": "AKC 상위 100위 견종의 원산지-성격 연관성 분석 결과",
            "total_breeds": len(breeds),
            "total_regions": len(region_analysis)
        },
        "region_analysis": region_analysis,
        "total_keyword_ranking": [
            {"rank": i+1, "keyword": kw, "count": cnt}
            for i, (kw, cnt) in enumerate(total_counter.most_common(30))
        ],
        "distinctive_by_region": distinctive,
        "breed_origin_map": [
            {
                "breed": name,
                "origin": origin,
                "region": region,
                "popularity_2025": next(
                    (b["popularity"].get("2025") for b in breeds if b["breed_name"] == name),
                    None
                )
            }
            for name, (origin, region) in sorted(
                origin_map.items(),
                key=lambda x: next(
                    (b["popularity"].get("2025", 999) for b in breeds if b["breed_name"] == x[0]),
                    999
                )
            )
        ]
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n\n💾 분석 결과 저장: {OUTPUT_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    analyze()
