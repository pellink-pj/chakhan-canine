// 강아지 품종 카드 컴포넌트 - 매칭 결과 표시용

import type { MatchResult } from "@/types/dog";

interface DogCardProps {
  result: MatchResult;
  rank: number;
}

/** 매칭 점수에 따른 배지 색상 */
function getScoreBadgeColor(score: number): string {
  if (score >= 85) return "bg-green-100 text-green-700 border-green-200";
  if (score >= 70) return "bg-amber-100 text-amber-700 border-amber-200";
  return "bg-gray-100 text-gray-600 border-gray-200";
}

/** 사이즈 한글 변환 */
function getSizeLabel(size: string): string {
  const sizeMap: Record<string, string> = {
    small: "소형",
    medium: "중형",
    large: "대형",
    giant: "초대형",
  };
  return sizeMap[size] ?? size;
}

/** 특성 점수 바 컴포넌트 */
function TraitBar({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500 w-16 shrink-0">{label}</span>
      <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full bg-amber-400 rounded-full transition-all"
          style={{ width: `${(value / 5) * 100}%` }}
        />
      </div>
      <span className="text-xs font-medium text-gray-600 w-4 text-right">
        {value}
      </span>
    </div>
  );
}

export default function DogCard({ result, rank }: DogCardProps) {
  const { dog, matchScore } = result;
  const badgeColor = getScoreBadgeColor(matchScore);

  return (
    <article className="bg-white rounded-2xl shadow-sm border border-amber-100 p-5 hover:shadow-md transition-shadow">
      {/* 순위 & 매칭 점수 */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-bold text-amber-500">#{rank}</span>
          {rank === 1 && <span className="text-xl">🏆</span>}
        </div>
        <div
          className={`px-3 py-1 rounded-full text-sm font-semibold border ${badgeColor}`}
        >
          매칭 {matchScore}%
        </div>
      </div>

      {/* 견종명 */}
      <div className="mb-1">
        <h3 className="text-lg font-bold text-gray-800">{dog.name_ko}</h3>
        <p className="text-sm text-gray-400">{dog.name_en}</p>
      </div>

      {/* 사이즈 & 태그 */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        <span className="px-2 py-0.5 bg-amber-50 text-amber-600 rounded-full text-xs font-medium border border-amber-100">
          {getSizeLabel(dog.physical.size)}
        </span>
        {dog.tags.map((tag) => (
          <span
            key={tag}
            className="px-2 py-0.5 bg-gray-50 text-gray-600 rounded-full text-xs border border-gray-100"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* 품종 설명 */}
      <p className="text-sm text-gray-600 leading-relaxed mb-4">
        {dog.description_ko}
      </p>

      {/* 특성 점수 바 */}
      <div className="space-y-1.5 pt-3 border-t border-gray-50">
        <TraitBar label="에너지" value={dog.traits_score.energy} />
        <TraitBar label="훈련성" value={dog.traits_score.trainability} />
        <TraitBar
          label="아파트"
          value={dog.traits_score.apartment_friendly}
        />
        <TraitBar
          label="아이친화"
          value={dog.traits_score.good_with_children}
        />
      </div>
    </article>
  );
}
