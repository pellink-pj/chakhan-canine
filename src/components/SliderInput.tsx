// 퀴즈 슬라이더 입력 컴포넌트 - 각 질문에 대한 1~5점 입력을 처리합니다.

"use client";

interface SliderInputProps {
  value: number;
  onChange: (value: number) => void;
  labelLow: string;
  labelHigh: string;
}

export default function SliderInput({
  value,
  onChange,
  labelLow,
  labelHigh,
}: SliderInputProps) {
  return (
    <div className="w-full">
      {/* 슬라이더 */}
      <input
        type="range"
        min={1}
        max={5}
        step={1}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full h-2 bg-amber-100 rounded-full appearance-none cursor-pointer
          [&::-webkit-slider-thumb]:appearance-none
          [&::-webkit-slider-thumb]:h-5
          [&::-webkit-slider-thumb]:w-5
          [&::-webkit-slider-thumb]:rounded-full
          [&::-webkit-slider-thumb]:bg-amber-500
          [&::-webkit-slider-thumb]:shadow-md
          [&::-webkit-slider-thumb]:cursor-pointer
          [&::-moz-range-thumb]:h-5
          [&::-moz-range-thumb]:w-5
          [&::-moz-range-thumb]:rounded-full
          [&::-moz-range-thumb]:bg-amber-500
          [&::-moz-range-thumb]:border-0"
      />

      {/* 눈금 표시 */}
      <div className="flex justify-between mt-1 px-0.5">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            className={`w-7 h-7 rounded-full text-sm font-medium transition-all ${
              value === n
                ? "bg-amber-500 text-white shadow-sm scale-110"
                : "bg-white text-gray-400 border border-gray-200 hover:border-amber-300"
            }`}
          >
            {n}
          </button>
        ))}
      </div>

      {/* 레이블 */}
      <div className="flex justify-between mt-2 text-xs text-gray-400">
        <span>{labelLow}</span>
        <span>{labelHigh}</span>
      </div>
    </div>
  );
}
