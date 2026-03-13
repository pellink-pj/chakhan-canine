// 강아지 매칭 알고리즘 - 사용자 선호도와 강아지 특성 점수를 비교하여 최적의 품종을 추천합니다.

import type { Dog, UserPreferences, MatchResult, DogTraitsScore } from "@/types/dog";

/**
 * 사용자 선호도를 강아지 특성 벡터로 변환합니다.
 * 사용자 입력을 강아지 traits_score와 비교 가능한 형태로 매핑합니다.
 * @param prefs - 사용자 라이프스타일 선호도
 * @returns 강아지 특성 점수 형식의 객체
 */
function mapPreferencesToTraits(prefs: UserPreferences): DogTraitsScore {
  return {
    energy: prefs.energy,
    shedding: prefs.shedding_tolerance,
    trainability: prefs.trainability_importance,
    barking: prefs.barking_tolerance,
    grooming_needs: prefs.grooming_willingness,
    good_with_children: prefs.children_at_home,
    good_with_other_pets: prefs.other_pets,
    apartment_friendly: prefs.apartment_living,
  };
}

/**
 * 두 특성 벡터 간의 유클리드 거리를 계산합니다.
 * 거리가 낮을수록 사용자와 강아지가 잘 맞는다는 의미입니다.
 * @param a - 강아지 특성 점수
 * @param b - 사용자 선호도를 변환한 특성 점수
 * @returns 유클리드 거리 값
 */
export function calculateEuclideanDistance(
  a: DogTraitsScore,
  b: DogTraitsScore
): number {
  const keys = Object.keys(a) as Array<keyof DogTraitsScore>;
  const sumOfSquares = keys.reduce((sum, key) => {
    const diff = a[key] - b[key];
    return sum + diff * diff;
  }, 0);
  return Math.sqrt(sumOfSquares);
}

/**
 * 유클리드 거리를 0~100 매칭 점수로 변환합니다.
 * 최대 가능한 거리(모든 특성이 최대 편차일 때)를 기준으로 정규화합니다.
 * @param distance - 유클리드 거리
 * @param numDimensions - 특성 차원 수
 * @returns 0~100 범위의 매칭 점수
 */
function distanceToScore(distance: number, numDimensions: number): number {
  // 각 차원의 최대 차이는 4 (1~5점 범위에서 최댓값 - 최솟값)
  const maxDistance = Math.sqrt(numDimensions * 4 * 4);
  const score = Math.round((1 - distance / maxDistance) * 100);
  return Math.max(0, Math.min(100, score));
}

/**
 * 사용자 선호도에 따라 강아지 품종을 매칭하여 점수 순으로 정렬된 결과를 반환합니다.
 * @param dogs - 전체 강아지 품종 목록
 * @param prefs - 사용자 라이프스타일 선호도
 * @param topN - 반환할 최대 결과 수 (기본값: 5)
 * @returns 매칭 점수 순으로 정렬된 결과 배열
 */
export function matchDogs(
  dogs: Dog[],
  prefs: UserPreferences,
  topN: number = 5
): MatchResult[] {
  // 입력 데이터 유효성 검사
  if (!dogs || dogs.length === 0) {
    return [];
  }

  const preferenceVector = mapPreferencesToTraits(prefs);
  const numDimensions = Object.keys(preferenceVector).length;

  const results: MatchResult[] = dogs
    .filter((dog) => dog.traits_score) // 특성 점수가 없는 항목 필터링
    .map((dog) => {
      const distance = calculateEuclideanDistance(
        dog.traits_score,
        preferenceVector
      );
      const matchScore = distanceToScore(distance, numDimensions);
      return { dog, distance, matchScore };
    });

  // 매칭 점수 내림차순 정렬 (높은 점수가 먼저)
  results.sort((a, b) => b.matchScore - a.matchScore);

  return results.slice(0, topN);
}
