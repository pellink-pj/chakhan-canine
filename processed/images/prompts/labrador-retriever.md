# 래브라도 리트리버 (Labrador Retriever)

- **breed_id**: `labrador-retriever`
- **분류**: 한국 인기 22위
- **카테고리**: kr_popular
- **저장 경로**: `processed/images/breeds/kr_popular/labrador-retriever.png`

## 견종 데이터

- 크기: 대형 · 24.9~36.3kg
- 키: 54.6~62.2cm
- 활동량 (raw_energy): 5점 → **달리는 모습 (최고 활동량)**
- 기질: active, friendly, outgoing

## 생성 프롬프트

```
medium-large Labrador Retriever with short dense coat, otter-like tail, kind warm face, running joyfully, all four legs in motion, ears in the wind, on plain concrete or asphalt ground, 2.5D illustration style, soft natural daylight, minimal background
```

## 사용처 (이미지 도구별 동일 프롬프트 OK)

- Adobe Firefly: 위 프롬프트 그대로 → Image 3 모델
- FLUX schnell (fal.ai): 위 프롬프트 그대로
- KlingAI: 위 프롬프트 그대로 (이전 가이드라인과 동일)

## Style Reference 사용 권장

첫 견종(말티즈)으로 톤 잡은 후, Style Reference 기능으로 다음 견종들 동일 톤 유지.

## 생성 후 메모

- [ ] 1차 시안 생성
- [ ] 선택 (베스트 1장)
- [ ] 파일 저장 경로 확인
- [ ] breeds.json image_local 매핑 확인
