# 🐕 착한 캐닌 (Chakhan Canine)

라이프스타일에 맞는 강아지를 추천하는 한국형 견종 매칭 서비스.

## 🌐 데모

👉 **[앱 사용해보기](https://chakhan-canine.streamlit.app)** *(배포 후 URL 업데이트)*

## 🚀 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📂 파일 구성

```
chakhan-canine/
├── app.py                    # Streamlit 메인 앱
├── recommender.py            # 추천 매칭 엔진
├── breed_enrichment.py       # 견종 데이터 가공 (점수·비용·태그·RAG)
├── process_data.py           # AKC 원본 → processed/ 변환
├── requirements.txt          # 의존성
├── processed/
│   ├── breeds.json           # 메인 추천 데이터 (293 견종)
│   ├── breed_articles.json   # 게시판/상세페이지용 영어 콘텐츠
│   ├── traits_guide.json     # AKC 점수 1~5점 기준
│   └── README.md             # 데이터 구조 가이드
└── result/                   # AKC 원본 크롤링 JSON
```

## 🎯 기능

- **3가지 질문**으로 라이프스타일 매칭 추천 (월 예산 / 산책 / 훈련 의지)
- **마음에 둔 견종 진단**: 이미 원하는 견종이 있으면 라이프스타일과 맞는지 매칭도로 표시
- **한국 인기 50견종** 우선 노출 (입양 희망자 기준)
- **현재 / 시니어 비용 분리**: 단두종·디스크·슬개골·고관절 위험 반영
- **외모 폴백 필터**: 크기·털 길이로 추가 필터

## 📊 데이터 출처

- 견종 정보: American Kennel Club (AKC)
- 한국 인기 순위: KB금융지주 / 농림축산식품부 통계 종합

---

## 🔧 AKC 크롤러 (참고용)

원본 데이터 갱신 시:

```bash
$ uv sync
```

* run

```bash
$ uv run main.py
```

## data structure

* root

```
data['settings']
```

* 견종이름

```
견종이름 = data['settings']['current_breed']
```

* 견종 정보

높이 단위: inchs
몸무게 단위: pounds

```
나라 = data['settings']['basics'][견종이름]['origin']

발견연도 = data['settings']['basics'][견종이름]['year_recognized']

수명 = data['settings']['basics'][견종이름]['life_expectancy']

최소 높이(female) = data['settings']['standards'][견종이름]['height_min_f']
최대 높이(female) = data['settings']['standards'][견종이름]['height_max_f']
최소 몸무게(female) = data['settings']['standards'][견종이름]['weight_min_f']
최대 몸무게(female) = data['settings']['standards'][견종이름]['weight_max_f']

최소 높이(male) = data['settings']['standards'][견종이름]['height_min_f']
최대 높이(male) = data['settings']['standards'][견종이름]['height_max_f']
최소 몸무게(male) = data['settings']['standards'][견종이름]['weight_min_f']
최대 몸무게(male) = data['settings']['standards'][견종이름]['weight_max_f']

사이즈 = data['settings']['standards'][견종이름]['size']

견종정보 = data['settings']['description'][견종이름]['akc_org_about']
```

* 건강정보

권장하는 건강 검사는 | 로 구분되어짐

```
건강정보 = data['settings']['health'][견종이름]['mp_health']

권장하는 건강 검사 = data['settings']['health'][견종이름]['tests_pipe_delimited_list']
```

* 특성 & 기질 정보

기질은 | 로 구분되어짐 

특성은 dict 타입으로 특성이름을 키로 가진다.

```
기질 = data['settings']['traits'][견종이름]['temperament']

특성{
    selected,
    choices,
    score,
    traits_url,
    traits,
    description,
    breed_group,
    type,
    low_value_1,
    middle_value_3,
    high_value_5,
} data['settings']['traits'][견종이름][adaptability_level, affectionate_with_family 등 특성 명칭]
```

* 히스토리

```
히스토리 = data['settings']['history'][견종이름]['akc_org_history']

히스토리 = data['settings']['breed']['history']['content']

히스토리에서 사용하는 슬라이드[{
    img_html,
    credit
}] = data['settings']['breed']['history']['slides']
```

* 사진

```
[{
    src,
    alt,
    caption
    credit
}] = data['settings']['breed']['media'][gallery]
```

```
표준사진 = data['settings']['breed']['standard'][image]
```

* 인기도

인기도는 작년부터 10개년 존재 
예를들어 현재 2025년도면 2024부터 2015까지 존재한

```
인기도 = data['settings']['breed_data']['basic'][popularity_연도]
```

### Needs to Keep
```
['setting']['breed_data']['basics']["THE DOG NAME"]['related_breeds_items']['temperament']

혈통 연관성 유사도 score 당 breed_group 에 특정 값으로 정도 강화 및 강도 약화 계산(정확도 높임)

['setting']['breed_data']['traits']["THE DOG NAME"]['traits']['각 모든 키 값']['score']
같은 위치 ['breed_group']
```