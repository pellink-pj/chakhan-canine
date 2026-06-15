"""
AKC 견종 크롤러 — 메인 실행

흐름:
  1. 기존 result/ → result_YYYYMMDD/ 백업
  2. AKC 홈에서 견종 목록 수집
  3. 각 견종 페이지 크롤링 (1초 간격, 에러 처리)
  4. 진행 상황 표시
  5. 실패 견종 따로 로깅
"""

import os
import time
import shutil
from datetime import datetime

from category import get_breeds
from detail import get_detail


def backup_existing(result_dir: str = "result") -> str | None:
    """기존 result/ 폴더를 result_YYYYMMDD/로 백업"""
    if not os.path.isdir(result_dir) or not os.listdir(result_dir):
        return None

    today = datetime.now().strftime("%Y%m%d")
    backup_dir = f"result_old_{today}"

    # 같은 날 백업이 있으면 _1, _2... 붙임
    suffix = 0
    final_backup = backup_dir
    while os.path.exists(final_backup):
        suffix += 1
        final_backup = f"{backup_dir}_{suffix}"

    shutil.move(result_dir, final_backup)
    return final_backup


def main():
    print("🐕 AKC 견종 크롤러 시작")
    print("━" * 50)

    # 1. 백업
    backup = backup_existing()
    if backup:
        print(f"✅ 옛 데이터 백업: ./{backup}/")
    else:
        print("ℹ  기존 result/ 폴더 없음 (처음 실행)")

    # 2. 견종 목록 수집
    print("\n📋 AKC 홈에서 견종 목록 수집 중...")
    try:
        breeds = get_breeds()
    except Exception as e:
        print(f"❌ 견종 목록 수집 실패: {e}")
        return

    total = len(breeds)
    print(f"✅ 총 {total}견종 발견\n")

    # 3. 크롤링 (1초 간격)
    success = 0
    failed = []
    start_time = time.time()

    for i, breed in enumerate(breeds, 1):
        result = get_detail(breed.url, breed.name)
        if result:
            success += 1
            status = "✓"
        else:
            failed.append(breed.name)
            status = "❌"

        # 진행 표시 (10마다 또는 처음/끝)
        elapsed = time.time() - start_time
        eta_sec = (elapsed / i) * (total - i) if i > 0 else 0
        eta_min = int(eta_sec / 60)
        print(f"  {status} [{i:3}/{total}] {breed.name:35} (남은 시간 약 {eta_min}분)")

        # Rate limiting (1초 간격, AKC 차단 방지)
        if i < total:
            time.sleep(1)

    # 4. 결과 요약
    print("\n" + "━" * 50)
    print(f"✅ 크롤링 완료")
    print(f"   성공: {success}견종")
    print(f"   실패: {len(failed)}견종")

    if failed:
        print(f"\n❌ 실패 견종 목록:")
        for name in failed:
            print(f"   - {name}")
        # 실패 견종 파일에 저장
        with open("failed_breeds.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(failed))
        print(f"\n   → failed_breeds.txt에 저장됨 (수동 재시도 가능)")

    total_min = int((time.time() - start_time) / 60)
    print(f"\n⏱  총 소요 시간: 약 {total_min}분")


if __name__ == "__main__":
    main()
