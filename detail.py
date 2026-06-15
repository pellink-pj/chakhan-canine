"""
AKC 견종 상세 페이지 크롤러
- User-Agent 박음 (봇 차단 회피)
- 에러 처리 + 재시도 1회
- 실패해도 다음 견종으로 진행
"""

import requests as rq
from bs4 import BeautifulSoup
import json
import os
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
}


def get_detail(url: str, breed_name: str, result_dir: str = "result", retry: int = 1) -> dict | None:
    """
    AKC 견종 페이지 → JSON 추출 → 파일 저장
    실패 시 None 반환 (호출자가 알 수 있게).
    """
    last_err = None
    for attempt in range(retry + 1):
        try:
            response = rq.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")
            raw_data_dom = soup.find("div", attrs={"data-js-component": "breedPage"})
            if not raw_data_dom:
                raise ValueError("breedPage 컴포넌트 없음 — 페이지 구조 변경됐을 가능성")

            raw_data = raw_data_dom.get("data-js-props", "{}")
            json_data = json.loads(raw_data)

            os.makedirs(result_dir, exist_ok=True)
            file_path = os.path.join(result_dir, f"{breed_name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

            return json_data
        except Exception as e:
            last_err = e
            if attempt < retry:
                time.sleep(2)  # 1회 재시도 전 2초 대기
                continue
            print(f"  ❌ {breed_name}: {type(e).__name__} — {e}")
            return None


if __name__ == "__main__":
    target_url = "https://www.akc.org/dog-breeds/beagle"
    get_detail(target_url, "Beagle")
