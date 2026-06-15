"""
견종별 이미지 생성 프롬프트 라이브러리 생성

- 한국 인기 30위 + 해외 히든 젬 9견종 = 40견종
- 활동량(raw_energy) 점수에 따라 포즈 분기:
    5점: 달리는 모습
    4점: 입 벌리고 헥헥(혀 내밈)
    1~3점: 일반 서있는 포즈
- 출력: /processed/images/prompts/{breed_id}.md
"""

import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("AKC_ROOT", "/Users/yeonly/akc-crawler"))
PROMPTS_DIR = ROOT / "processed" / "images" / "prompts"
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

# ─── 공통 스타일 토큰 (단순, 브랜드 일관성) ──────────────────
COMMON_STYLE = "2.5D illustration style, soft natural daylight, minimal background"

# ─── 배경 (단순화) ───────────────────────────────────────────
BACKGROUND = "on plain concrete or asphalt ground"

# ─── 활동량별 포즈 분기 (짧게) ──────────────────────────────
POSE_BY_ENERGY = {
    5: "running joyfully, all four legs in motion, ears in the wind",
    4: "standing alert with mouth open, tongue out panting happily",
    3: "standing calmly with a gentle expression",
    2: "standing in a calm composed pose",
    1: "sitting comfortably with a serene expression",
}

# ─── 견종별 외형 토큰 보정 (특정 견종은 일반 묘사로 부족) ────
BREED_VISUAL_OVERRIDES = {
    "maltese": "small pure white silky long-coated Maltese dog, dark round eyes, black nose",
    "poodle-toy": "small Toy Poodle with curly textured coat, alert expression, refined features",
    "poodle-miniature": "Miniature Poodle with curly groomed coat, intelligent expression",
    "poodle-standard": "elegant Standard Poodle with curly coat, athletic build, refined posture",
    "pomeranian": "tiny fluffy Pomeranian with double coat fox-like face, alert expression, fluffy tail curled over back",
    "korean-jindo-dog": "medium Korean Jindo Dog, double coat, prick ears, fox-like alert expression, curled tail",
    "shih-tzu": "small Shih Tzu with long flowing double coat, large round eyes, short muzzle",
    "bichon-frise": "small Bichon Frise with fluffy white powder-puff coat, round teddy bear face, dark eyes",
    "chihuahua": "tiny Chihuahua with apple-head shape, large bat-like ears, big expressive eyes",
    "golden-retriever": "medium Golden Retriever with feathered golden coat, kind warm expression, friendly eyes",
    "yorkshire-terrier": "tiny Yorkshire Terrier with long silky blue-and-tan coat, small confident face",
    "japanese-spitz": "small Japanese Spitz with pure white double coat, pointed ears, fox-like face, smiling expression",
    "pembroke-welsh-corgi": "Pembroke Welsh Corgi with short legs, long body, large upright ears, fox-like face",
    "cardigan-welsh-corgi": "Cardigan Welsh Corgi with long tail, short legs, long body, large upright ears",
    "dachshund": "long-bodied short-legged Dachshund, expressive face, long droopy ears",
    "beagle": "Beagle with tricolor short coat, long droopy ears, sweet pleading expression",
    "french-bulldog": "compact French Bulldog with bat ears, flat short muzzle, muscular small body",
    "border-collie": "athletic Border Collie with medium double coat, intense intelligent gaze, alert ears",
    "shiba-inu": "Shiba Inu with double coat, prick ears, curled tail, fox-like face, confident expression",
    "pekingese": "small Pekingese with long flowing coat, flat face, lion-like mane around face",
    "miniature-schnauzer": "Miniature Schnauzer with wiry coat, distinctive beard and eyebrows, alert expression",
    "cocker-spaniel": "Cocker Spaniel with long feathered ears, silky coat, soft melting expression",
    "labrador-retriever": "medium-large Labrador Retriever with short dense coat, otter-like tail, kind warm face",
    "coton-de-tulear": "small Coton de Tulear with pure white cotton-like fluffy coat, dark round eyes, sweet face",
    "italian-greyhound": "elegant Italian Greyhound, slender build, fine short coat, refined delicate features",
    "pug": "small Pug with curled tail, deeply wrinkled face, flat muzzle, expressive large eyes",
    "boston-terrier": "small Boston Terrier with tuxedo black-and-white markings, large round eyes, erect ears",
    "samoyed": "fluffy white Samoyed with thick double coat, smiling expression, dark eyes",
    "papillon": "small Papillon with large butterfly-shaped ears with long feathering, fine silky coat",
    "cavalier-king-charles-spaniel": "Cavalier King Charles Spaniel with long feathered ears, silky tricolor or ruby coat, gentle eyes",
    "siberian-husky": "athletic Siberian Husky with thick double coat, blue or bi-colored eyes, alert face, wolf-like features",
    # 해외 히든 젬
    "german-shorthaired-pointer": "athletic German Shorthaired Pointer with liver-and-white short coat, lean muscular build, intense gaze",
    "cane-corso": "muscular Cane Corso with short dense coat, large powerful build, alert noble expression",
    "australian-shepherd": "Australian Shepherd with medium double coat, merle or tricolor pattern, intelligent expression, sometimes heterochromia",
    "boxer": "muscular Boxer with short fawn or brindle coat, square muzzle, expressive alert face",
    "bernese-mountain-dog": "large Bernese Mountain Dog with thick tricolor coat (black, white, rust), gentle giant expression",
    "great-dane": "tall majestic Great Dane with short smooth coat, elegant noble bearing, gentle expression",
    "havanese": "small Havanese with long silky wavy coat, expressive dark eyes, joyful playful face",
    "english-springer-spaniel": "English Springer Spaniel with long feathered ears, liver-and-white coat, athletic build, kind eyes",
    "miniature-american-shepherd": "Miniature American Shepherd with medium double coat, merle pattern often, intelligent alert expression",
}


def build_prompt(breed: dict) -> str:
    """견종 데이터 → 통합 프롬프트 한 줄"""
    breed_id = breed["_id"]
    scores = breed.get("scores", {})
    energy = scores.get("exercise_needs", {}).get("raw_energy", 3)

    # 외형 토큰 (오버라이드 우선, 없으면 데이터 기반 generic)
    visual = BREED_VISUAL_OVERRIDES.get(breed_id)
    if not visual:
        size_kr = {"small": "small", "medium": "medium-sized", "large": "large", "giant": "very large"}.get(
            breed.get("size_category"), "medium-sized"
        )
        breed_name = breed["breed_name"]
        visual = f"{size_kr} {breed_name} dog, natural breed-typical appearance"

    pose = POSE_BY_ENERGY.get(energy, POSE_BY_ENERGY[3])

    prompt = f"{visual}, {pose}, {BACKGROUND}, {COMMON_STYLE}"
    return prompt


def build_md(breed: dict) -> str:
    """견종별 .md 파일 내용 생성"""
    breed_id = breed["_id"]
    kr_name = breed.get("kr_name") or breed["breed_name"]
    breed_name = breed["breed_name"]
    scores = breed.get("scores", {})
    energy = scores.get("exercise_needs", {}).get("raw_energy", 3)

    # 카테고리 결정
    if breed.get("kr_popularity_tier") == "popular":
        category = "kr_popular"
        rank_info = f"한국 인기 {breed['kr_popularity_rank']}위"
    elif breed.get("kr_popularity_tier") == "unique" and breed.get("akc_popularity_rank"):
        category = "intl_popular"
        rank_info = f"해외 인기 (AKC) {breed['akc_popularity_rank']}위 · 한국 unique"
    else:
        category = "kr_popular"
        rank_info = f"한국 {breed.get('kr_popularity_rank', '?')}위"

    pose_desc = {
        5: "달리는 모습 (최고 활동량)",
        4: "헥헥(입 벌리고 혀 내밈)",
        3: "차분히 서있기",
        2: "조용히 서있기",
        1: "편안히 앉기",
    }.get(energy, "차분히 서있기")

    temperament = ", ".join(breed.get("temperament", [])[:5])
    weight = breed.get("weight_kr", "정보 없음")
    height = breed.get("height_kr", "정보 없음")

    prompt = build_prompt(breed)

    return f"""# {kr_name} ({breed_name})

- **breed_id**: `{breed_id}`
- **분류**: {rank_info}
- **카테고리**: {category}
- **저장 경로**: `processed/images/breeds/{category}/{breed_id}.png`

## 견종 데이터

- 크기: {breed.get("size_category_kr", "—")} · {weight}
- 키: {height}
- 활동량 (raw_energy): {energy}점 → **{pose_desc}**
- 기질: {temperament}

## 생성 프롬프트

```
{prompt}
```

## 사용처 (이미지 도구별 동일 프롬프트 OK)

- Adobe Firefly: 위 프롬프트 그대로 → Image 3 모델
- FLUX schnell (fal.ai): 위 프롬프트 그대로
- KlingAI: 위 프롬프트 그대로 (이전 가이드라인과 동일)

## Style Reference 사용 권장

첫 견종(말티즈)으로 톤 잡은 후, Style Reference 기능으로 다음 견종들 동일 톤 유지.

## 생성 후 메모

- [ ] 1차 시안 생성
- [ ] 선택 (베스트 1장)
- [ ] 파일 저장 경로 확인
- [ ] breeds.json image_local 매핑 확인
"""


def main():
    with open(ROOT / "processed" / "breeds.json", encoding="utf-8") as f:
        data = json.load(f)
    breeds = data["breeds"]

    # 한국 인기 30위
    kr_popular = [b for b in breeds if b.get("kr_popularity_tier") == "popular"]
    # 해외 히든 젬 (AKC 30위 + 한국 unique)
    hidden_gems = [
        b for b in breeds
        if b.get("akc_popularity_rank") and b["akc_popularity_rank"] <= 30
        and b.get("kr_popularity_tier") == "unique"
    ]

    target = kr_popular + hidden_gems
    target.sort(key=lambda b: (
        b.get("kr_popularity_tier") != "popular",
        b.get("kr_popularity_rank") or b.get("akc_popularity_rank") or 999
    ))

    print(f"📦 총 {len(target)}견종 프롬프트 생성")
    print(f"   - 한국 인기: {len(kr_popular)}견종")
    print(f"   - 해외 히든 젬: {len(hidden_gems)}견종\n")

    for breed in target:
        breed_id = breed["_id"]
        out = PROMPTS_DIR / f"{breed_id}.md"
        out.write_text(build_md(breed), encoding="utf-8")
        kr_name = breed.get("kr_name") or breed["breed_name"]
        energy = breed.get("scores", {}).get("exercise_needs", {}).get("raw_energy", 3)
        pose_emoji = {5: "🏃", 4: "😮‍💨", 3: "🧍", 2: "🧍", 1: "🪑"}.get(energy, "🧍")
        print(f"  {pose_emoji} {kr_name:30} ({breed_id}) — 활동량 {energy}점")

    print(f"\n✅ 완료 → {PROMPTS_DIR}")


if __name__ == "__main__":
    main()
