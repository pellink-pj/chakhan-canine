// 앱 상단 네비게이션 헤더 컴포넌트

import Link from "next/link";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-amber-100 shadow-sm">
      <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* 로고 */}
        <Link
          href="/"
          className="flex items-center gap-2 font-bold text-xl text-amber-600 hover:text-amber-700 transition-colors"
        >
          <span className="text-2xl">🐾</span>
          <span>PetLink</span>
          <span className="text-xs font-normal text-gray-400 ml-1">펫링크</span>
        </Link>

        {/* 네비게이션 메뉴 */}
        <nav className="flex items-center gap-1">
          <Link
            href="/"
            className="px-3 py-1.5 rounded-lg text-sm font-medium text-gray-600 hover:text-amber-600 hover:bg-amber-50 transition-colors"
          >
            홈
          </Link>
          <Link
            href="/quiz"
            className="px-4 py-1.5 rounded-lg text-sm font-medium bg-amber-500 text-white hover:bg-amber-600 transition-colors"
          >
            강아지 찾기
          </Link>
        </nav>
      </div>
    </header>
  );
}
