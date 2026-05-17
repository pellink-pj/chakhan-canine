# 견종 데이터 가이드

AKC 크롤링 데이터를 한국 시장 + AI 추천 시스템용으로 정제한 데이터셋.

## 📂 파일 구성

| 파일 | 용도 | 크기 |
|---|---|---|
| `breeds.json` | 메인 추천 데이터 (사람이 읽기 좋게 들여쓰기) | ~2.2 MB |
| `breeds.ndjson` | MongoDB import용 (한 줄에 견종 1마리) | ~1.7 MB |
| `breed_articles.json` | 게시판/상세페이지용 영어 콘텐츠 | ~2 MB |
| `breed_articles.ndjson` | 같은 내용 NDJSON | ~2 MB |
| `traits_guide.json` | AKC traits 점수 1~5점 의미 설명 | ~9 KB |

**`.json` vs `.ndjson`**: 같은 내용. `.json`은 전체가 하나의 JSON 객체 (개발 중 확인용), `.ndjson`은 한 줄에 견종 하나 (MongoDB/스트림 import용).

---

## 📊 단위 가이드

데이터에 나오는 숫자들의 단위:

| 필드 | 단위 |
|---|---|
| `cost_estimate.monthly_krw_min/max` | **원 (KRW)** |
| `cost_estimate.breakdown.food/grooming/...` | **원 (KRW)** |
| `scores.exercise_needs.daily_walk_minutes` | **분 (minutes)** |
| `weight_kg_min/max` | **킬로그램 (kg)** |
| `height_cm_min_male/max_male/min_female/max_female` | **센티미터 (cm)** |
| `weight_kr`, `height_kr` | 한국어 표현 (예: "약 3.2kg", "17.8~22.9cm") |

---

## 🎯 추천 시스템 핵심 필드

### 1. `scores` — 사용자 매칭용 점수 카테고리

모든 점수는 AKC 원본 1~5점을 기반으로 가공.

```javascript
scores: {
  shedding: {           // 털날림
    raw: 1,             // AKC 원점수 1~5
    level: "very_low",  // 5단계 등급
    level_kr: "매우 낮음"
  },
  barking: { ... },     // 짖음
  grooming: {           // 그루밍 빈도
    raw: 4,
    frequency_kr: "주 2~3회"  // 권장 빈도
  },
  exercise_needs: {     // 운동량
    raw_energy: 3,
    daily_walk_minutes: 45,    // 권장 산책 시간 (분)
    level_kr: "보통"
  },
  training_difficulty: {  // 훈련 강도
    difficulty_score: 3,  // 1=매우 쉬움, 5=매우 어려움
    note: "꾸준한 반복 훈련 필요. 일반적 수준"
  },
  friendliness: {       // 친화력
    avg_score: 3.5,     // 4개 항목 평균
    raw_with_family: 5,
    raw_with_strangers: 3,
    raw_with_dogs: 3,
    raw_with_children: 5
  }
}
```

### 2. `cost_estimate` — 한국 시장 월 양육비 추정

```javascript
cost_estimate: {
  monthly_krw_min: 174250,  // 월 최소 (원)
  monthly_krw_max: 246000,  // 월 최대 (원)
  level: "medium",          // low/medium/high/very_high
  level_kr: "보통",
  breakdown: {
    food:          50000,   // 식비
    grooming:      50000,   // 그루밍
    medical:       45000,   // 의료비 (기본 + 견종 특이 검사)
    supplies:      30000,   // 용품 (간식, 패드, 장난감)
    training_care: 30000    // 훈련/케어 (난이도 기반)
  },
  factors: {
    size: "small",
    grooming_score: 4,
    health_tests_count: 3,
    training_difficulty: 3
  }
}
```

**비용 등급 기준:**
- `low`: 월 평균 ~20만원
- `medium`: 20~35만원
- `high`: 35~50만원
- `very_high`: 50만원+

### 3. `lifestyle_tags` — 빠른 필터링용

가능한 태그 목록:
```
small_dog, large_dog
low_shedding, high_shedding
quiet, vocal
hypoallergenic
apartment_friendly, needs_yard_or_long_walks
good_for_beginners, requires_experienced_owner
low_energy, high_energy
good_with_kids, good_with_other_dogs
budget_friendly, expensive_to_keep
```

### 4. `rag_chunks` — 벡터 임베딩용 한국어 청크

주제별 자연어 텍스트. MongoDB Atlas Vector Search 또는 별도 벡터 DB에 임베딩.

```javascript
rag_chunks: [
  { topic: "intro",                topic_kr: "기본 소개",            text: "..." },
  { topic: "personality",          topic_kr: "성격과 기질",          text: "..." },
  { topic: "shedding_grooming",    topic_kr: "털날림과 관리",        text: "..." },
  { topic: "barking",              topic_kr: "짖음 정도",            text: "..." },
  { topic: "training",             topic_kr: "훈련",                 text: "..." },
  { topic: "exercise",             topic_kr: "운동량과 산책",        text: "..." },
  { topic: "cost_korea",           topic_kr: "한국 양육 비용",       text: "..." },
  { topic: "korean_lifestyle_fit", topic_kr: "한국 라이프스타일 적합도", text: "..." }
]
```

---

## 🇰🇷 한국 인기 분류 (`kr_popularity_tier`)

| Tier | 범위 | 의미 |
|---|---|---|
| `popular` | 한국 1~30위 | 흔히 보는 견종 (소형견 위주) |
| `less_popular` | 한국 31~50위 | 매니아층 (대형·특수견 위주) |
| `unique` | 50위 밖 | 한국에서 잘 안 키우는 견종 (외국 인기견종 추천 시 활용) |

**한국 인기 출처**: KB금융지주/농림축산식품부 통계 종합

**AKC에 없는 한국 인기견종 (4종 제외)**:
- 믹스견 (3위), 말티푸 (14위) — AKC 미등록
- 풍산개 (43위), 삽살개 (44위) — AKC 미등록 한국 토종

---

## 🐕 견종 변종 (`variety_group`, `variety`)

같은 견종의 변종을 묶음. 추천 시 중복 제거에 활용.

| `variety_group` | 견종들 |
|---|---|
| `poodle` | Toy, Miniature, Standard |
| `welsh-corgi` | Pembroke, Cardigan |

```javascript
// 같은 그룹은 한 견종으로 묶어서 추천
const deduped = _.uniqBy(breeds, b => b.variety_group || b._id)
```

---

## 📈 AKC traits 점수 1~5 의미

자세한 기준은 `traits_guide.json` 참조. 요약:

| Trait | 1점 | 3점 | 5점 |
|---|---|---|---|
| `shedding_level` | 거의 안 빠짐 | 보통 | 매우 많이 빠짐 |
| `barking_level` | 알릴 때만 | 가끔 | 매우 많이 짖음 |
| `coat_grooming_frequency` | 월 1회 | 주 1회 | 매일 |
| `energy_level` | 누워있기 좋아함 | 보통 | 매우 활동적 |
| `trainability_level` | 고집 셈 | 협조적 | 학습 의지 강함 |
| `affectionate_with_family` | 독립적 | 친밀 | 매우 애정 |
| `openness_to_strangers` | 경계심 강함 | 보통 | 누구나 친구 |
| `good_with_other_dogs` | 비추천 | 감독 필요 | 잘 어울림 |
| `good_with_young_children` | 비추천 | 감독 필요 | 잘 어울림 |
| `mental_stimulation_needs` | 누워있어도 됨 | 보통 | 일/활동 필요 |

---

## 🤖 MongoDB 사용 예시

### Import
```bash
mongoimport --db dog_recommender --collection breeds \
  --file breeds.ndjson

mongoimport --db dog_recommender --collection breed_articles \
  --file breed_articles.ndjson
```

### 추천 인덱스
```javascript
db.breeds.createIndex({ kr_popularity_tier: 1 })
db.breeds.createIndex({ "cost_estimate.level": 1 })
db.breeds.createIndex({ "scores.exercise_needs.raw_energy": 1 })
db.breeds.createIndex({ "scores.training_difficulty.difficulty_score": 1 })
db.breeds.createIndex({ lifestyle_tags: 1 })  // multikey
```

### 추천 쿼리 예시
```javascript
// "월 25만원 이하, 산책 30분 이내, 훈련 자신 없음" 사용자
db.breeds.find({
  "cost_estimate.monthly_krw_max":          { $lte: 250000 },
  "scores.exercise_needs.daily_walk_minutes": { $lte: 30 },
  "scores.training_difficulty.difficulty_score": { $lte: 2 },
  lifestyle_tags: "apartment_friendly"
}).sort({ kr_popularity_rank: 1 })

// 외국 인기견종 추천 (한국에서 안 흔한)
db.breeds.find({
  kr_popularity_tier: "unique",
  akc_popularity_rank: { $lte: 30 }
})
```

---

## 🔍 RAG (의미 검색) 활용

### 흐름
```
사용자 질문 "털 안 빠지는 작은 강아지"
  → 임베딩 모델이 벡터로 변환
  → 모든 견종의 rag_chunks와 벡터 유사도 비교
  → 가장 가까운 chunk들 검색 (예: 말티즈/비숑/푸들의 shedding_grooming chunk)
  → LLM이 컨텍스트로 받아 답변 생성
```

### MongoDB Atlas Vector Search 인덱스
```javascript
db.breeds.createSearchIndex({
  name: "breed_rag_vector",
  type: "vectorSearch",
  definition: {
    fields: [{
      type: "vector",
      path: "rag_chunks.embedding",
      numDimensions: 1536,  // OpenAI ada-002 기준
      similarity: "cosine"
    }]
  }
})
```

> 임베딩은 데이터에 미리 들어있지 않음. 별도 임베딩 파이프라인에서 각 chunk의 `text`를 벡터로 변환해 `embedding` 필드를 추가해야 함.

---

## 📝 사용자 질문지 설계 (라이프스타일 매칭)

추천 시스템에서 사용자에게 물을 수 있는 질문 예시:

### Q1. 월 양육비 예산은?
```
□ ~20만원       → cost_estimate.level: "low"
□ 20~35만원    → "medium"
□ 35~50만원    → "high"
□ 50만원 이상  → "very_high"
```

### Q2. 하루에 얼마나 산책시킬 수 있나요?
```
□ 20분 이내    → exercise_needs.daily_walk_minutes <= 20
□ 30~45분     → <= 45
□ 1시간 이상   → <= 75
□ 2시간 이상   → 제한 없음
```

### Q3. 훈련에 시간을 들일 수 있나요?
```
□ 거의 어려워요          → training_difficulty <= 2
□ 기본 훈련만             → <= 3
□ 적극적으로 할 수 있어요 → 제한 없음

(질문지에 함께 표시할 안내문)
"훈련을 잘 시키면 견종이 자신감과 안정감을 얻어 짖음·분리불안 등 문제 행동이
크게 줄어듭니다. 보호자와의 신뢰 관계도 깊어져 가족 전체가 행복해집니다."
```

### Q4. 털 빠지는 정도 어디까지 괜찮으세요?
```
□ 전혀 안 빠졌으면 좋겠어요  → lifestyle_tags: "low_shedding"
□ 어느 정도는 괜찮아요
□ 신경 안 써요
```

### Q5. 주거 환경은?
```
□ 아파트/빌라  → lifestyle_tags: "apartment_friendly", barking <= 3
□ 단독주택      → 제한 없음
```

---

## 🛠 데이터 재생성

```bash
cd akc-crawler
python3 process_data.py
```

`result/` 폴더의 견종 JSON 파일들을 모두 다시 처리해서 `processed/` 폴더 갱신.

원본 크롤링 데이터 갱신은 `main.py`/`detail.py` 참고.
