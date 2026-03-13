// 강아지 매칭 결과 페이지 - URL 쿼리 파라미터에서 선호도를 읽어 매칭 알고리즘 실행

import { Suspense } from "react";
import ResultsContent from "./ResultsContent";

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <div className="text-4xl mb-3 animate-bounce">🐾</div>
            <p className="text-gray-500">매칭 중...</p>
          </div>
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
