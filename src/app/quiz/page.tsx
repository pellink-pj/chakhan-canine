// 강아지 MBTI 퀴즈 페이지 - 사용자 라이프스타일 선호도 입력

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import SliderInput from "@/components/SliderInput";
import { QUIZ_QUESTIONS } from "@/lib/quizData";
import type { UserPreferences } from "@/types/dog";

/** 초기 선호도 값 - 모든 항목을 중간값(3)으로 설정 */
const INITIAL_PREFERENCES: UserPreferences = {
  energy: 3,
  shedding_tolerance: 3,
  trainability_importance: 3,
  barking_tolerance: 3,
  grooming_willingness: 3,
  children_at_home: 3,
  other_pets: 3,
  apartment_living: 3,
};

export default function QuizPage() {
  // 현재 질문 인덱스 상태
  const [currentStep, setCurrentStep] = useState(0);
  // 사용자 선호도 상태
  const [preferences, setPreferences] =
    useState<UserPreferences>(INITIAL_PREFERENCES);

  const router = useRouter();
  const totalSteps = QUIZ_QUESTIONS.length;
  const currentQuestion = QUIZ_QUESTIONS[currentStep];

  /** 단일 선호도 값 업데이트 */
  const handlePreferenceChange = (
    key: keyof UserPreferences,
    value: number
  ) => {
    setPreferences((prev) => ({ ...prev, [key]: value }));
  };

  /** 다음 질문으로 이동 */
  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  };

  /** 이전 질문으로 이동 */
  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  /** 퀴즈 완료 - 결과 페이지로 이동 (쿼리 파라미터로 선호도 전달) */
  const handleSubmit = () => {
    const params = new URLSearchParams(
      Object.entries(preferences).map(([key, value]) => [key, String(value)])
    );
    router.push(`/results?${params.toString()}`);
  };

  const progressPercent = Math.round(((currentStep + 1) / totalSteps) * 100);

  return (
    <div className="max-w-xl mx-auto px-4 py-10">
      {/* 헤더 */}
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-1">
          🐾 강아지 매칭 퀴즈
        </h1>
        <p className="text-sm text-gray-400">
          {currentStep + 1} / {totalSteps} 질문
        </p>
      </div>

      {/* 진행 바 */}
      <div className="w-full h-2 bg-gray-100 rounded-full mb-8 overflow-hidden">
        <div
          className="h-full bg-amber-400 rounded-full transition-all duration-500"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* 질문 카드 */}
      <div className="bg-white rounded-2xl shadow-sm border border-amber-100 p-6 mb-6">
        {/* 아이콘 및 질문 */}
        <div className="text-4xl mb-3 text-center">{currentQuestion.icon}</div>
        <h2 className="text-xl font-bold text-gray-800 text-center mb-2">
          {currentQuestion.question_ko}
        </h2>
        <p className="text-sm text-gray-400 text-center mb-8 leading-relaxed">
          {currentQuestion.description_ko}
        </p>

        {/* 슬라이더 입력 */}
        <SliderInput
          value={preferences[currentQuestion.id]}
          onChange={(val) => handlePreferenceChange(currentQuestion.id, val)}
          labelLow={currentQuestion.labels.low}
          labelHigh={currentQuestion.labels.high}
        />
      </div>

      {/* 이전 / 다음 버튼 */}
      <div className="flex gap-3">
        {currentStep > 0 && (
          <button
            type="button"
            onClick={handleBack}
            className="flex-1 py-3 rounded-xl border border-gray-200 text-gray-600 font-medium hover:bg-gray-50 transition-colors"
          >
            ← 이전
          </button>
        )}
        {currentStep < totalSteps - 1 ? (
          <button
            type="button"
            onClick={handleNext}
            className="flex-1 py-3 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600 transition-colors"
          >
            다음 →
          </button>
        ) : (
          <button
            type="button"
            onClick={handleSubmit}
            className="flex-1 py-3 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600 transition-colors"
          >
            결과 보기 🐕
          </button>
        )}
      </div>

      {/* 단계별 도트 표시 */}
      <div className="flex justify-center gap-1.5 mt-6">
        {QUIZ_QUESTIONS.map((_, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setCurrentStep(idx)}
            className={`h-2 rounded-full transition-all ${
              idx === currentStep
                ? "w-6 bg-amber-500"
                : idx < currentStep
                  ? "w-2 bg-amber-300"
                  : "w-2 bg-gray-200"
            }`}
            aria-label={`질문 ${idx + 1}로 이동`}
          />
        ))}
      </div>
    </div>
  );
}
