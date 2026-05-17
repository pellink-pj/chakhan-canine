# 📖 데이터 사전 (Data Dictionary)

> **프로젝트**: AKC 견종 데이터 정제 파이프라인  
> **대상 파일**: `processed/` 폴더 내 JSON 파일들  
> **공통 키**: 모든 파일은 `breed_name_url`로 서로 연결됨

---

## 📁 파일 구조 개요

```
processed/
├── breeds_core.json          # 견종 기본 신원 + 신체 정보
├── breeds_traits.json        # 성격·특성 점수 (1~5)
├── breeds_descriptions.json  # 텍스트 설명 (HTML 제거)
├── breeds_popularity.json    # 인기 순위 + 트렌드
├── breeds_safety.json        # 안전 정보 (한국 법령 포함)
└── traits_guide.json         # traits 점수 기준표 (공통 참고용)
```

---

## 1. `breeds_core.json` — 견종 기본 정보

### 최상위 구조
```json
{
  "_meta": { ... },
  "breeds": [ { 각 견종 객체 }, ... ]
}
```

### 각 견종 객체 키

| 키 | 타입 | 설명 | 예시 |
|----|------|------|------|
| `breed_name_url` | string | URL용 견종 이름. **공통 연결 키** | `"french-bulldog"` |
| `breed_name` | string | 공식 견종 이름 | `"French Bulldog"` |
| `akc_code` | string | AKC 내부 코드 | `"305"` |
| `breed_group` | string | AKC 견종 그룹 | `"Non-Sporting Group"` |
| `origin` | string | 원산지 국가/지역 (AKC 원문) | `"England"` |
| `origin_region` | string | 원산지를 묶은 지역 그룹 (한국어) | `"영국/아일랜드"` |
| `year_recognized` | string | AKC 공식 인정 연도 | `"1898"` |
| `life_expectancy` | string | 평균 수명 범위 | `"10-12 years"` |
| `size` | string | 크기 분류 | `"Small"` / `"Medium"` / `"Large"` |
| `height_display` | string | 키 범위 표시 텍스트 | `"11-13 inches"` |
| `weight_display` | string | 몸무게 범위 표시 텍스트 | `"under 28 pounds"` |
| `height_min_m` | string | 수컷 최소 키 (인치) | `"11"` |
| `height_max_m` | string | 수컷 최대 키 (인치) | `"13"` |
| `height_min_f` | string | 암컷 최소 키 (인치) | `"11"` |
| `height_max_f` | string | 암컷 최대 키 (인치) | `"13"` |
| `weight_min` | string | 최소 몸무게 (파운드) | `"28"` |
| `weight_max` | string | 최대 몸무게 (파운드) | `"28"` |
| `colors.standard` | string[] | 공인 표준 털 색상 목록 | `["Black", "White"]` |
| `colors.alternate` | string[] | 공인 비표준 털 색상 목록 | `["Sable"]` |
| `markings.standard` | string[] | 공인 표준 무늬 목록 | `["White Markings"]` |
| `markings.alternate` | string[] | 공인 비표준 무늬 목록 | `[]` |
| `images.standard` | string | 대표 이미지 URL | `"https://..."` |
| `images.gallery` | string[] | 갤러리 이미지 URL 목록 | `["https://..."]` |
| `breed_club_name` | string | 견종 전문 클럽 이름 | `"French Bulldog Club of America"` |
| `breed_club_url` | string | 전문 클럽 웹사이트 | `"https://..."` |
| `breed_rescue_url` | string | 구조/입양 단체 웹사이트 | `"https://..."` |

### `origin_region` 분류 기준

| 값 | 포함 국가 |
|----|----------|
| `영국/아일랜드` | England, Scotland, Wales, Ireland |
| `독일권` | Germany, Austria, Switzerland |
| `프랑스/벨기에` | France, Belgium |
| `북미` | United States, Canada |
| `동아시아` | Japan, China, Korea |
| `북유럽` | Norway, Sweden, Finland, Iceland, Denmark |
| `러시아/동유럽` | Russia, Poland, Hungary, Czech Republic |
| `남유럽` | Italy, Spain, Portugal, Malta |
| `중동/아프리카` | Egypt, Africa, Sahel Region |
| `중앙아시아/티베트` | Tibet, China/Tibet |
| `호주` | Australia |
| `기타(...)` | 위 분류에 없는 지역 |

---

## 2. `breeds_traits.json` — 성격/특성 점수

### 각 견종 객체 키

| 키 | 타입 | 설명 |
|----|------|------|
| `breed_name_url` | string | 공통 연결 키 |
| `temperament` | string[] | 대표 기질 키워드 (AKC 원문) | 
| `scores` | object | 특성 점수 모음 (아래 상세 참조) |
| `coat.length` | string[] | 털 길이 (`Short` / `Medium` / `Long`) |
| `coat.type` | string[] | 털 종류 (아래 참조) |

### `scores` 내 각 항목 (모두 1~5점 정수)

> 점수 의미는 `traits_guide.json` 참조. 숫자가 높을수록 해당 특성이 강함.

| 키 | 한국어 이름 | 1점 의미 | 5점 의미 |
|----|------------|---------|---------|
| `adaptability_level` | 적응력 | 루틴이 필요함 | 매우 잘 적응 |
| `affectionate_with_family` | 가족 애정도 | 독립적 | 매우 애정적 |
| `barking_level` | 짖음 빈도 | 거의 안 짖음 | 매우 자주 짖음 |
| `coat_grooming_frequency` | 그루밍 필요도 | 월 1회 | 매일 필요 |
| `good_with_young_children` | 어린이 친화성 | 비추천 | 어린이와 잘 어울림 |
| `drooling_level` | 침 흘림 | 거의 없음 | 항상 흘림 |
| `energy_level` | 에너지 수준 | 소파형 | 매우 활발 |
| `good_with_other_dogs` | 다견 친화성 | 비추천 | 잘 어울림 |
| `mental_stimulation_needs` | 정신적 자극 필요도 | 여유로움 | 일/활동 필요 |
| `openness_to_strangers` | 낯선 사람 친화성 | 경계심 강함 | 누구에게나 친근 |
| `playfulness_level` | 장난기 | 요청할 때만 | 쉬지 않고 놀고 싶어함 |
| `shedding_level` | 털 빠짐 | 거의 없음 | 털 폭탄 |
| `trainability_level` | 훈련 용이성 | 고집이 셈 | 훈련 매우 잘 됨 |
| `watchdogprotective_nature` | 경비/보호 본능 | 경비 역할 없음 | 매우 경계함 |

### `coat.type` 가능한 값

`Smooth`, `Double`, `Wavy`, `Curly`, `Wiry`, `Silky`, `Rough`, `Corded`, `Hairless`

---

## 3. `breeds_descriptions.json` — 설명 텍스트

> ⚠️ 모든 텍스트는 HTML 태그 제거됨. 원본 AKC 영어 텍스트.

| 키 | 타입 | 설명 | 평균 길이 |
|----|------|------|---------|
| `breed_name_url` | string | 공통 연결 키 | - |
| `summary` | string | 한 줄 소개 (blurb 기반) | ~150자 |
| `about` | string | 중간 길이 설명 (about 기반) | ~500자 |
| `care.health` | string | 건강 관리 정보 | ~400자 |
| `care.nutrition` | string | 영양/식이 정보 | ~400자 |
| `care.grooming` | string | 그루밍 방법 | ~300자 |
| `care.exercise` | string | 운동 필요량 | ~300자 |
| `care.training` | string | 훈련 방법 | ~400자 |
| `history` | string | 견종 역사 | ~1000자 |
| `did_you_know` | string[] | 흥미로운 사실 목록 | 2~5개 |
| `health_tests` | string[] | AKC 권장 건강 검사 목록 | 1~5개 |

---

## 4. `breeds_popularity.json` — 인기 순위

| 키 | 타입 | 설명 | 예시 |
|----|------|------|------|
| `breed_name_url` | string | 공통 연결 키 | `"french-bulldog"` |
| `us_rank` | object | 미국 AKC 연도별 순위 | `{"2021": 2, "2025": 1}` |
| `us_trend` | string | 미국 순위 추세 | `"rising"` / `"stable"` / `"falling"` |
| `us_trend_delta` | integer | 순위 변화량 (양수=상승, 음수=하락) | `1` |
| `kr_rank` | object | 한국 연도별 순위 (있을 경우) | `{"2024": 1}` |
| `kr_trend` | string | 한국 순위 추세 | `"rising"` / `"stable"` / `"falling"` |

### `us_trend` 계산 기준
- `rising`: 2025 순위 숫자 < 2021 순위 숫자 (더 높은 순위로 올라감)
- `falling`: 2025 순위 숫자 > 2021 순위 숫자 (순위 밀림)
- `stable`: 변화량이 ±2 이내

---

## 5. `breeds_safety.json` — 안전 정보

| 키 | 타입 | 설명 | 예시 |
|----|------|------|------|
| `breed_name_url` | string | 공통 연결 키 | `"rottweiler"` |
| `child_safety_score` | integer (1~5) | 어린이 안전성 점수 | `3` |
| `child_safety_label` | string | 점수에 대한 라벨 | `"With Supervision"` |
| `aggression_score` | integer (1~5) | 공격성 추정 점수 (높을수록 주의) | `4` |
| `is_dangerous_breed_kr` | boolean | 한국 법령상 맹견 여부 | `true` |
| `dangerous_breed_note` | string | 맹견일 경우 법적 의무 설명 | `"외출 시 입마개 착용 의무..."` |
| `recommended_for.children_under_5` | boolean | 5세 미만 영아와 함께 가능 여부 | `false` |
| `recommended_for.other_dogs` | boolean | 다른 개와 함께 가능 여부 | `true` |
| `recommended_for.first_time_owners` | boolean | 초보 견주에게 적합 여부 | `false` |
| `recommended_for.apartment` | boolean | 아파트(소형 주거) 적합 여부 | `true` |

### `child_safety_label` 매핑

| 점수 | 라벨 |
|------|------|
| 1 | `"Not Recommended"` |
| 2 | `"Use Caution"` |
| 3 | `"With Supervision"` |
| 4 | `"Generally Good"` |
| 5 | `"Good With Children"` |

### 자동 계산 로직 요약

| 필드 | 계산 방법 |
|------|----------|
| `child_safety_score` | `traits.good_with_young_children` 점수 그대로 |
| `aggression_score` | `(watchdogprotective_nature + (6 - openness_to_strangers)) / 2` 반올림 |
| `children_under_5` | `child_safety_score >= 4` |
| `other_dogs` | `good_with_other_dogs >= 3` |
| `first_time_owners` | `trainability_level >= 3` |
| `apartment` | `size ∈ {Small, Medium}` AND `energy_level <= 3` |

---

## 6. `traits_guide.json` — 점수 기준표 (공통 참고)

| 키 | 설명 |
|----|------|
| `traits.{키}.name` | 특성 영어 이름 |
| `traits.{키}.group` | 특성 그룹 (`Family Life` / `Character` / `Social` / `Physical`) |
| `traits.{키}.description` | 이 특성이 무엇을 의미하는지 설명 |
| `traits.{키}.scale.1` | 1점 레이블 |
| `traits.{키}.scale.3` | 3점 레이블 |
| `traits.{키}.scale.5` | 5점 레이블 |
| `traits.{키}.type` | `"radio"` (1~5점) 또는 `"checkbox"` (다중 선택) |
| `traits.{키}.choices` | checkbox형일 때 선택 가능한 값 목록 |
