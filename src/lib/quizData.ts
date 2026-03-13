// 강아지 MBTI 퀴즈 질문 데이터

import type { QuizQuestion } from "@/types/dog";

/** 퀴즈 질문 목록 */
export const QUIZ_QUESTIONS: QuizQuestion[] = [
  {
    id: "energy",
    question_ko: "얼마나 활동적인 강아지를 원하시나요?",
    description_ko: "산책, 운동, 놀이에 들일 수 있는 시간과 에너지를 생각해보세요.",
    icon: "⚡",
    labels: {
      low: "조용하고 느긋한",
      high: "활발하고 에너지 넘치는",
    },
  },
  {
    id: "shedding_tolerance",
    question_ko: "털 빠짐을 얼마나 감수할 수 있나요?",
    description_ko: "집안 청소 빈도와 털 알레르기 여부를 고려해보세요.",
    icon: "🐾",
    labels: {
      low: "털이 거의 안 빠지길 원함",
      high: "많이 빠져도 괜찮음",
    },
  },
  {
    id: "trainability_importance",
    question_ko: "훈련이 잘 되는 강아지를 원하시나요?",
    description_ko: "기본 훈련이나 특별 훈련의 중요도를 선택해주세요.",
    icon: "🎓",
    labels: {
      low: "훈련성은 중요하지 않음",
      high: "훈련 잘 되는 게 중요함",
    },
  },
  {
    id: "barking_tolerance",
    question_ko: "짖음 소리를 얼마나 허용할 수 있나요?",
    description_ko: "아파트 또는 이웃과 가까이 거주한다면 중요한 요소입니다.",
    icon: "🔊",
    labels: {
      low: "조용한 강아지를 원함",
      high: "많이 짖어도 괜찮음",
    },
  },
  {
    id: "grooming_willingness",
    question_ko: "그루밍에 얼마나 시간을 투자할 수 있나요?",
    description_ko: "빗질, 목욕, 미용 등 털 관리에 들이는 노력을 생각해보세요.",
    icon: "✂️",
    labels: {
      low: "관리가 거의 필요 없길 원함",
      high: "자주 그루밍해 줄 수 있음",
    },
  },
  {
    id: "children_at_home",
    question_ko: "집에 어린아이가 있나요?",
    description_ko: "어린이와의 친화성이 높은 강아지를 추천할 수 있습니다.",
    icon: "👶",
    labels: {
      low: "어린이 없음",
      high: "어린 아이가 있음",
    },
  },
  {
    id: "other_pets",
    question_ko: "다른 반려동물과 함께 살고 있나요?",
    description_ko: "다른 반려동물과의 친화성을 고려합니다.",
    icon: "🐱",
    labels: {
      low: "다른 반려동물 없음",
      high: "여러 반려동물 있음",
    },
  },
  {
    id: "apartment_living",
    question_ko: "어떤 주거 환경에서 살고 있나요?",
    description_ko: "아파트나 좁은 공간에서는 적합한 견종이 따로 있습니다.",
    icon: "🏠",
    labels: {
      low: "넓은 마당 있는 주택",
      high: "아파트 / 원룸",
    },
  },
];
