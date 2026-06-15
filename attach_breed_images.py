"""
견종 이미지 파일 → breeds.json 자동 매핑 + 한글 메타데이터 박기

Co가 /processed/images/ 폴더에 넣은 PNG 파일을:
  1. breeds.json의 image_local 필드에 자동 박음
  2. PNG 메타데이터(tEXt 청크)에 한글 이름·설명 박음 → Adobe Bridge·Lightroom 인식
  3. macOS xattr Spotlight Comment 박음 → Finder 검색 가능

파일명 규칙:
  "Maltese.png"            → maltese
  "Yorkshire Terrier.png"  → yorkshire-terrier
  "Toy Poodle.png"         → poodle-toy (alias 사용)
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AKC_ROOT", "/Users/yeonly/akc-crawler"))
IMAGES_DIR = ROOT / "processed" / "images"
BREEDS_JSON = ROOT / "processed" / "breeds.json"

# 변종 alias — 사람이 쓰는 자연스러운 이름 → breeds.json _id
ALIASES = {
    "toy-poodle": "poodle-toy",
    "miniature-poodle": "poodle-miniature",
    "standard-poodle": "poodle-standard",
}


def filename_to_breed_id(filename: str) -> str:
    """파일명 → breed slug 변환 + alias 적용"""
    name = filename.rsplit(".", 1)[0]
    slug = name.lower().replace(" ", "-").replace("_", "-")
    return ALIASES.get(slug, slug)


def write_png_metadata(image_path: Path, kr_name: str, breed_name: str, kr_tier: str | None):
    """PNG tEXt 청크에 한글 메타데이터 박기 (Pillow 사용)"""
    try:
        from PIL import Image, PngImagePlugin
    except ImportError:
        print("  ⚠ Pillow 미설치 — PNG 메타데이터 스킵 (pip install Pillow)")
        return False

    if image_path.suffix.lower() != ".png":
        return False

    try:
        img = Image.open(image_path)
        meta = PngImagePlugin.PngInfo()
        meta.add_text("Title", kr_name)
        meta.add_text("Description", f"{kr_name} ({breed_name})")
        meta.add_text("Subject", kr_name)
        meta.add_text("Author", "Mungmate")
        if kr_tier:
            meta.add_text("Category", kr_tier)
        # 원본 덮어쓰기
        img.save(image_path, "PNG", pnginfo=meta)
        return True
    except Exception as e:
        print(f"  ⚠ PNG 메타데이터 실패 ({image_path.name}): {e}")
        return False


def write_macos_spotlight_comment(image_path: Path, kr_name: str, breed_name: str):
    """macOS Spotlight Comment 박기 (xattr + osascript)"""
    if sys.platform != "darwin":
        return False
    try:
        comment = f"{kr_name} {breed_name}"
        # AppleScript로 Spotlight Comment (kMDItemFinderComment) 박기
        script = f'''
        on run argv
            set theFile to POSIX file (item 1 of argv) as alias
            tell application "Finder"
                set comment of theFile to (item 2 of argv)
            end tell
        end run
        '''
        subprocess.run(
            ["osascript", "-e", script, str(image_path), comment],
            capture_output=True,
            timeout=5,
        )
        return True
    except Exception:
        return False


def main():
    # 1. 이미지 파일 수집
    image_files = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp"]:
        image_files.extend(IMAGES_DIR.glob(ext))
    image_files = [f for f in image_files if not f.name.startswith(".")]

    print(f"📦 발견된 이미지: {len(image_files)}개\n")

    # 2. breeds.json 읽기
    with open(BREEDS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    breeds_by_id = {b["_id"]: b for b in data["breeds"]}

    # 3. 파일별 매핑 + 메타데이터 박기
    matched = 0
    meta_written = 0
    unmatched_files = []

    for img in sorted(image_files):
        breed_id = filename_to_breed_id(img.name)
        breed = breeds_by_id.get(breed_id)

        if not breed:
            unmatched_files.append((img.name, breed_id))
            continue

        # breeds.json image_local 박기
        breed["image_local"] = f"images/{img.name}"
        matched += 1

        kr_name = breed.get("kr_name") or breed["breed_name"]
        breed_name = breed["breed_name"]
        kr_tier = breed.get("kr_popularity_tier")

        # 메타데이터 박기
        png_ok = write_png_metadata(img, kr_name, breed_name, kr_tier)
        macos_ok = write_macos_spotlight_comment(img, kr_name, breed_name)
        if png_ok or macos_ok:
            meta_written += 1

        tag = "📝" if (png_ok and macos_ok) else "✓"
        print(f"  {tag} {kr_name:30} → {img.name}")

    # 4. 미매칭 파일 표시
    if unmatched_files:
        print(f"\n⚠ 매칭 실패 ({len(unmatched_files)}개):")
        for fname, slug in unmatched_files:
            print(f"    - {fname} (변환: {slug})")
        print("  → ALIASES 테이블에 추가하거나 파일명 수정 필요")

    # 5. 저장
    with open(BREEDS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    ndjson_path = ROOT / "processed" / "breeds.ndjson"
    if ndjson_path.exists():
        with open(ndjson_path, "w", encoding="utf-8") as f:
            for breed in data["breeds"]:
                f.write(json.dumps(breed, ensure_ascii=False) + "\n")

    print(f"\n✅ 완료")
    print(f"   매칭 성공:     {matched}개")
    print(f"   메타데이터 박음: {meta_written}개 (PNG tEXt + macOS Spotlight)")


if __name__ == "__main__":
    main()
