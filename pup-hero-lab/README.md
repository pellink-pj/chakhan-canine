# 🐶 Pup Hero Lab

견종 추천 데이터를 기반으로 가상 강아지를 키워보는 다마고치 스타일 실험 앱.
"10분영웅키우기" 게임의 컨셉 검증용 프로토타입.

## 🎮 기능 (Phase 1)

- 견종 선택 (293견종 중 한국 인기 위주 정렬)
- 4가지 인터랙션: 먹이 주기 🍖 / 산책 🚶 / 훈련 🎓 / 놀이 🎾
- 강아지 스탯 시스템: 행복도 / 배고픔 / 에너지 / 친밀도
- **Claude Haiku 4.5**로 견종 성격을 반영한 대사 자동 생성
- 시간 경과에 따른 자연스러운 스탯 변화 (passive decay)

## 📁 파일 구조

```
pup-hero-lab/
├── app.py              # Streamlit 메인 앱
├── tamagotchi.py       # 게임 로직 (스탯, 인터랙션)
├── claude_client.py    # Claude API 호출 + 견종 페르소나 프롬프트
├── data/breeds.json    # 견종 데이터 (chakhan-canine에서 복사)
├── requirements.txt
└── README.md
```

## 🚀 로컬 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Anthropic API key 설정

방법 A: 환경변수 (간단)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

방법 B: Streamlit secrets 파일 (배포 시 동일하게 사용)
```bash
mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-..."' > .streamlit/secrets.toml
```

⚠️ **`.streamlit/secrets.toml`은 절대 git에 commit하지 마세요!** (`.gitignore`에 포함됨)

### 3. 실행

```bash
streamlit run app.py
```

## ☁️ Streamlit Cloud 배포

1. GitHub에 push (위 `.gitignore` 덕분에 secrets.toml은 안 올라감)
2. https://share.streamlit.io 에서 새 앱 생성 → repo 선택
3. **앱 Settings → Secrets** 메뉴에서 API key 입력:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Deploy

## 🎯 다음 단계 아이디어

- [ ] 픽셀아트 강아지 sprite 추가
- [ ] 시간 흐름에 따른 강아지 성장 (강아지 → 성견 → 시니어)
- [ ] 랜덤 이벤트 (낯선 사람 등장, 다른 개와 마주침 등)
- [ ] 자유 대화 모드 (질문하면 강아지가 답변)
- [ ] 메인 견종 추천 앱(chakhan-canine)과 연동

## 🔗 관련 프로젝트

- **chakhan-canine**: 본 프로토타입의 견종 데이터 출처. 견종 추천 메인 앱
- **10분영웅키우기**: 본 프로토타입의 컨셉이 적용될 메인 게임 프로젝트
