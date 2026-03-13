// 결과 페이지 내용 컴포넌트 - useSearchParams를 사용하므로 클라이언트 컴포넌트

"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import DogCard from "@/components/DogCard";
import { matchDogs } from "@/lib/matching";
import type { Dog, UserPreferences, MatchResult } from "@/types/dog";

/** URL 쿼리 파라미터에서 사용자 선호도를 파싱합니다 */
function parsePreferences(searchParams: URLSearchParams): UserPreferences {
  const getNum = (key: string, fallback = 3): number => {
    const val = Number(searchParams.get(key));
    return isNaN(val) || val < 1 || val > 5 ? fallback : val;
  };

  return {
    energy: getNum("energy"),
    shedding_tolerance: getNum("shedding_tolerance"),
    trainability_importance: getNum("trainability_importance"),
    barking_tolerance: getNum("barking_tolerance"),
    grooming_willingness: getNum("grooming_willingness"),
    children_at_home: getNum("children_at_home"),
    other_pets: getNum("other_pets"),
    apartment_living: getNum("apartment_living"),
  };
}

export default function ResultsContent() {
  const searchParams = useSearchParams();
  // 매칭 결과 상태
  const [results, setResults] = useState<MatchResult[]>([]);
  // 로딩 상태
  const [loading, setLoading] = useState(true);
  // 에러 상태
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 강아지 데이터 로드 및 매칭 실행
    async function loadAndMatch() {
      try {
        setLoading(true);
        setError(null);

        // public 폴더의 JSON 데이터를 fetch로 로드
        const response = await fetch("/data/optimized_dogs_master.json");
        if (!response.ok) {
          throw new Error("강아지 데이터를 불러오는 데 실패했습니다.");
        }

        const dogs: Dog[] = await response.json();

        // 강아지 데이터 유효성 검사
        if (!Array.isArray(dogs) || dogs.length === 0) {
          throw new Error("강아지 데이터가 올바르지 않습니다.");
        }

        // 사용자 선호도 파싱
        const prefs = parsePreferences(searchParams);

        // 매칭 알고리즘 실행 - 상위 5개 결과 반환
        const matched = matchDogs(dogs, prefs, 5);
        setResults(matched);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다."
        );
      } finally {
        setLoading(false);
      }
    }

    loadAndMatch();
  }, [searchParams]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-center">
          <div className="text-4xl mb-3 animate-bounce">🐾</div>
          <p className="text-gray-500">최적의 강아지를 찾는 중...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto px-4 py-20 text-center">
        <div className="text-4xl mb-4">😢</div>
        <p className="text-gray-600 mb-6">{error}</p>
        <Link
          href="/quiz"
          className="inline-block px-6 py-3 bg-amber-500 text-white rounded-xl hover:bg-amber-600 transition-colors"
        >
          다시 시도하기
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      {/* 헤더 */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-3">🎉</div>
        <h1 className="text-2xl font-bold text-gray-800 mb-2">
          나에게 맞는 강아지 TOP 5
        </h1>
        <p className="text-sm text-gray-400">
          라이프스타일 분석을 바탕으로 가장 잘 맞는 강아지 품종을 추천해드립니다.
        </p>
      </div>

      {/* 결과 카드 목록 */}
      {results.length > 0 ? (
        <div className="space-y-4 mb-8">
          {results.map((result, idx) => (
            <DogCard key={result.dog.id} result={result} rank={idx + 1} />
          ))}
        </div>
      ) : (
        <div className="text-center py-10 text-gray-400">
          <p>매칭 결과를 찾을 수 없습니다.</p>
        </div>
      )}

      {/* 다시 하기 버튼 */}
      <div className="flex flex-col sm:flex-row gap-3 justify-center">
        <Link
          href="/quiz"
          className="px-6 py-3 rounded-xl bg-amber-500 text-white font-semibold text-center hover:bg-amber-600 transition-colors"
        >
          다시 테스트하기
        </Link>
        <Link
          href="/"
          className="px-6 py-3 rounded-xl border border-gray-200 text-gray-600 font-medium text-center hover:bg-gray-50 transition-colors"
        >
          홈으로 가기
        </Link>
      </div>
    </div>
  );
}
