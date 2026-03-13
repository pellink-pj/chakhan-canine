// PetLink 홈/랜딩 페이지

import Link from "next/link";

/** 서비스 특징 데이터 */
const FEATURES = [
  {
    icon: "🐕",
    title: "강아지 MBTI 매칭",
    description:
      "나의 라이프스타일과 성격에 맞는 강아지 품종을 AI 알고리즘으로 추천해드립니다.",
  },
  {
    icon: "🤝",
    title: "펫시터 매칭",
    description:
      "훈련된 펫시터와 반려견 주인을 위치 기반으로 매칭하여 안심하고 맡길 수 있습니다.",
  },
  {
    icon: "🚨",
    title: "긴급 AI 챗봇",
    description:
      "산책 중 응급 상황 발생 시 RAG 기반 AI가 즉시 응급처치 가이드를 제공합니다.",
  },
  {
    icon: "��",
    title: "AI 인증 프로필",
    description:
      "강아지 기질 프로파일링과 펫시터 자격 인증을 AI가 검증하여 신뢰도를 높입니다.",
  },
];

export default function HomePage() {
  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* 히어로 섹션 */}
      <section className="text-center py-16 px-4">
        <div className="text-6xl mb-4">🐾</div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4 leading-tight">
          나에게 딱 맞는{" "}
          <span className="text-amber-500">강아지</span>를
          <br />
          찾아드립니다
        </h1>
        <p className="text-lg text-gray-500 mb-8 max-w-xl mx-auto leading-relaxed">
          PetLink는 AI 기반 강아지 매칭 플랫폼입니다.
          <br />
          나의 라이프스타일에 맞는 최적의 견종을 추천받고,
          <br />
          믿을 수 있는 펫시터와 연결되세요.
        </p>
        <Link
          href="/quiz"
          className="inline-flex items-center gap-2 px-8 py-4 bg-amber-500 text-white text-lg font-semibold rounded-2xl shadow-md hover:bg-amber-600 hover:shadow-lg transition-all active:scale-95"
        >
          <span>강아지 찾기 시작하기</span>
          <span>→</span>
        </Link>
      </section>

      {/* 서비스 특징 카드 섹션 */}
      <section className="py-10">
        <h2 className="text-2xl font-bold text-gray-700 text-center mb-8">
          PetLink 주요 기능
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {FEATURES.map((feature) => (
            <div
              key={feature.title}
              className="bg-white rounded-2xl p-6 shadow-sm border border-amber-100 hover:shadow-md transition-shadow"
            >
              <div className="text-3xl mb-3">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-500 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA 배너 */}
      <section className="py-10">
        <div className="bg-gradient-to-r from-amber-400 to-amber-500 rounded-3xl p-8 text-center text-white shadow-md">
          <h2 className="text-2xl font-bold mb-3">
            지금 바로 나만의 강아지를 찾아보세요 🐶
          </h2>
          <p className="text-amber-100 mb-6 text-sm">
            8가지 라이프스타일 질문에 답하면 AI가 최적의 견종을 추천해드립니다.
          </p>
          <Link
            href="/quiz"
            className="inline-block px-6 py-3 bg-white text-amber-600 font-semibold rounded-xl hover:bg-amber-50 transition-colors"
          >
            무료로 시작하기
          </Link>
        </div>
      </section>
    </div>
  );
}
