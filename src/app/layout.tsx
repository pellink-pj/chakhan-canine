// 앱 전체 레이아웃 - PetLink 메타데이터 및 기본 폰트 설정

import type { Metadata, Viewport } from "next";
import "./globals.css";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "PetLink 펫링크 | 나에게 맞는 강아지 찾기",
  description:
    "AI 기반 반려견 매칭 플랫폼 PetLink. 나의 라이프스타일에 딱 맞는 강아지 품종을 추천받으세요.",
  keywords: ["강아지 추천", "반려견 매칭", "펫링크", "강아지 MBTI"],
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#f59e0b",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased bg-amber-50/30 min-h-screen font-sans">
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
