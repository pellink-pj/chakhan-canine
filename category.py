"""
AKC 홈에서 견종 목록 수집
"""

import requests as rq
from bs4 import BeautifulSoup
from pydantic import BaseModel

from detail import HEADERS

BASE_URL = "https://www.akc.org/"


class Breed(BaseModel):
    name: str
    url: str


def get_breeds() -> list[Breed]:
    response = rq.get(BASE_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    breed_search = soup.find(id="homepage-hero-breed-search")
    if not breed_search:
        raise RuntimeError("AKC 홈에서 견종 검색 드롭다운 못 찾음 — 페이지 구조 변경됐을 가능성")

    breeds = []
    for breed in breed_search.find_all("option"):
        name = breed.text.strip()
        url = breed.get("value", "").strip()
        if name and url:
            breeds.append(Breed(name=name, url=url))
    return breeds


if __name__ == "__main__":
    breeds = get_breeds()
    print(f"총 {len(breeds)}견종 발견")
    for breed in breeds[:5]:
        print(f"  - {breed.name}: {breed.url}")
