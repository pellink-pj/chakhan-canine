/* MungMate app — sample data (from the chakhan-canine breed dataset + journey.py).
   Korean-market reinterpreted AKC traits. Scores are 1–5.
   No emoji: avatars use a monogram, insight cards rely on tone color. */

window.MM_DATA = {
  // ── Readiness diagnostic (후킹 질문) — provocative, assumption-busting ──
  diagnostic: [
    {
      q: '작은 강아지가 키우기 더 쉬울 거라 생각하세요?',
      hint: '말티즈·푸들 같은 인기 소형견을 떠올리며',
      options: [
        { label: '네, 작을수록 쉽죠', value: 'yes' },
        { label: '꼭 그렇진 않을 것 같아요', value: 'no' },
      ],
      truth: '사실, 소형견일수록 짖음·분리불안이 잦고 슬개골 탈구 위험이 높아요. 크기와 난이도는 별개예요.',
    },
    {
      q: '이사 갈 집이 펫 금지면, 다른 집을 찾을 여유가 있으세요?',
      hint: '한국 임대 시장의 현실을 생각하며',
      options: [
        { label: '네, 강아지가 우선이에요', value: 'yes' },
        { label: '솔직히 자신 없어요', value: 'no' },
      ],
      truth: '주거 불안정은 한국 유기의 큰 원인이에요. 입양은 10년 이상의 약속이에요.',
    },
    {
      q: '귀여운 강아지가 손을 물면, 어떻게 하시겠어요?',
      hint: '모든 강아지는 물 수 있어요',
      options: [
        { label: '훈련으로 고쳐나가요', value: 'yes' },
        { label: '많이 당황스러울 것 같아요', value: 'no' },
      ],
      truth: '문제 행동은 견종 탓이 아니라 훈련의 문제예요. 준비된 보호자에겐 해결 가능한 과제예요.',
    },
  ],

  // ── Breed recommendations (matching result) ──
  breeds: [
    {
      id: 'sheltie',
      name: '셔틀랜드 쉽독',
      en: 'Shetland Sheepdog',
      nick: '셸티',
      mono: '셔',
      match: 92,
      rank: 29,
      size: '소형~중형',
      life: '12–14년',
      temperament: ['영리함', '활발함', '다정함'],
      summary: '스코틀랜드 셰틀랜드 제도 출신의 영리한 목양견. 가족에게 깊이 헌신하고 학습 의지가 매우 강해요.',
      costMonthly: '15–25만원',
      traits: [
        { label: '짖음', score: 5, word: '매우 높음', tone: 'hope' },
        { label: '훈련 가능성', score: 5, word: '매우 쉬움', tone: 'good' },
        { label: '활동량', score: 4, word: '높음', tone: 'hope' },
        { label: '가족 친화', score: 5, word: '매우 다정', tone: 'good' },
        { label: '털 빠짐', score: 3, word: '보통', tone: 'brand' },
        { label: '낯선 사람', score: 2, word: '경계함', tone: 'brand' },
      ],
      messages: [
        { tone: 'hope', title: '원래 잘 짖지만, 훈련으로 컨트롤 가능해요',
          text: '타고난 경계심으로 짖음이 많은 편이에요. 하지만 학습 의지가 강해서, 꾸준한 훈련으로 짖음을 컨트롤할 수 있어요. 공동주택에서도 충분히 함께 살 수 있어요.' },
        { tone: 'hope', title: '활동량이 많은 견종이에요',
          text: '하루 1시간 이상의 산책·놀이가 필요해요. 충분히 운동시켜주면 실내에선 차분히 지내요.' },
        { tone: 'good', title: '아이와 가족에게 다정한 견종이에요',
          text: '가족과의 친밀도가 높고, 어린 자녀와도 잘 어울려요. 안전한 가족견 후보예요.' },
      ],
      founder: true,
    },
    {
      id: 'border-collie',
      name: '보더 콜리',
      en: 'Border Collie',
      nick: 'BC',
      mono: '보',
      match: 84,
      rank: 26,
      size: '중형',
      life: '12–15년',
      temperament: ['에너지', '다정함', '천재견'],
      summary: '세계에서 가장 영리한 견종. 일(Job)이 필요한 워킹독이라 충분한 자극이 핵심이에요.',
      costMonthly: '18–30만원',
      traits: [
        { label: '짖음', score: 3, word: '보통', tone: 'brand' },
        { label: '훈련 가능성', score: 5, word: '매우 쉬움', tone: 'good' },
        { label: '활동량', score: 5, word: '매우 높음', tone: 'hope' },
        { label: '가족 친화', score: 4, word: '다정', tone: 'good' },
      ],
      messages: [
        { tone: 'hope', title: '에너지가 매우 높은 워킹독이에요',
          text: '운동과 두뇌 자극이 부족하면 문제 행동이 생겨요. 산책 + 노즈워크 + 트릭 훈련을 함께 해주세요.' },
        { tone: 'good', title: '다른 강아지와 잘 어울려요',
          text: '사회성이 좋아 강아지 놀이터에서도 무리 없이 어울려요.' },
      ],
      founder: false,
    },
    {
      id: 'maltese',
      name: '말티즈',
      en: 'Maltese',
      nick: '말티즈',
      mono: '말',
      match: 71,
      rank: 1,
      size: '초소형',
      life: '12–15년',
      temperament: ['애교', '활발함', '예민함'],
      summary: '한국에서 가장 인기 있는 견종. 사랑스럽지만 데이터는 짖음·슬개골 위험을 경고해요.',
      costMonthly: '12–20만원',
      traits: [
        { label: '짖음', score: 4, word: '높음', tone: 'hope' },
        { label: '훈련 가능성', score: 3, word: '보통', tone: 'brand' },
        { label: '활동량', score: 3, word: '보통', tone: 'brand' },
        { label: '가족 친화', score: 5, word: '매우 다정', tone: 'good' },
      ],
      messages: [
        { tone: 'hope', title: '생각보다 잘 짖는 편이에요',
          text: '인기와 달리 경계 짖음이 잦아요. 어릴 때부터 사회화·분리불안 훈련을 해주면 충분히 관리돼요.' },
        { tone: 'caution', title: '슬개골 탈구를 주의해주세요',
          text: '소형견 특성상 무릎 관절이 약해요. 미끄럼 방지 매트와 체중 관리가 중요해요.' },
      ],
      founder: false,
    },
  ],

  // ── Founder testimony (from breed_messages.py) ──
  founderTestimony:
    '멍메이트 창업자의 셸티도 짖음이 매우 높은 견종이에요. 5년 훈련으로 지금은 짖지 않고, 물지 않고, 아이가 와서 눈을 찔러도 가만히 있어요. 좋은 견종이 따로 있는 게 아니라, 좋은 보호자가 만듭니다.',
};
