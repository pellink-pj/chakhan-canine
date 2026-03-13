// 개 품종 데이터 모델 타입 정의

/** 개의 신체적 특성 */
export interface DogPhysical {
  size: "small" | "medium" | "large" | "giant";
  coat_length: string[];
  coat_type: string[];
}

/** 개의 특성 점수 (1~5점 척도) */
export interface DogTraitsScore {
  energy: number;            // 에너지 수준
  shedding: number;          // 털 빠짐 정도
  trainability: number;      // 훈련 용이성
  barking: number;           // 짖음 빈도
  grooming_needs: number;    // 그루밍 필요도
  good_with_children: number; // 아이와의 친화성
  good_with_other_pets: number; // 다른 반려동물과의 친화성
  apartment_friendly: number; // 아파트 적합도
}

/** 개 품종 전체 데이터 */
export interface Dog {
  id: string;
  name_en: string;
  name_ko: string;
  physical: DogPhysical;
  traits_score: DogTraitsScore;
  description_ko: string;
  tags: string[];
}

/** 사용자 라이프스타일 선호도 입력 (1~5점 척도) */
export interface UserPreferences {
  energy: number;            // 원하는 에너지 수준
  shedding_tolerance: number; // 털 빠짐 허용도 (5: 많이 허용)
  trainability_importance: number; // 훈련 용이성 중요도
  barking_tolerance: number; // 짖음 허용도 (5: 많이 허용)
  grooming_willingness: number; // 그루밍 의지 (5: 자주 해줄 수 있음)
  children_at_home: number;  // 집에 아이가 있는 정도 (5: 어린 아이 있음)
  other_pets: number;        // 다른 반려동물 보유 정도 (5: 여러 마리)
  apartment_living: number;  // 아파트 거주 여부 (5: 아파트 거주)
}

/** 매칭 결과 - 개 품종과 거리 점수 */
export interface MatchResult {
  dog: Dog;
  distance: number; // 유클리드 거리 (낮을수록 더 잘 맞음)
  matchScore: number; // 0~100 매칭 점수 (높을수록 더 잘 맞음)
}

/** 퀴즈 질문 인터페이스 */
export interface QuizQuestion {
  id: keyof UserPreferences;
  question_ko: string;
  description_ko: string;
  icon: string;
  labels: {
    low: string;
    high: string;
  };
}
