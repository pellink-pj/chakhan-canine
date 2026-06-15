"""
견종 JSON 파일들의 traits(특성 지표) 구조가 모두 동일한지 확인하는 스크립트

사용법:
  python check_traits_consistency.py --folder ./json파일들이_있는_폴더
  python check_traits_consistency.py  (현재 폴더에서 실행)
"""

import json
import os
import argparse
from collections import defaultdict

# 비교할 메타 필드 목록 (각 trait 항목이 갖는 키들)
META_FIELDS = ["traits", "description", "breed_group", "type",
               "low_value_1", "middle_value_3", "high_value_5", "traits_url"]


def load_json_files(folder):
    """폴더 내 모든 JSON 파일 로드"""
    files = {}
    for fname in os.listdir(folder):
        if fname.endswith(".json"):
            fpath = os.path.join(folder, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                files[fname] = data
            except Exception as e:
                print(f"  ⚠️  [{fname}] 로드 실패: {e}")
    return files


def extract_traits(data, fname):
    """JSON에서 traits 섹션 추출"""
    try:
        breed_data = data["settings"]["breed_data"]["traits"]
        # 견종 키 (예: "australian-cattle-dog")
        breed_key = list(breed_data.keys())[0]
        traits = breed_data[breed_key].get("traits", {})
        return breed_key, traits
    except (KeyError, IndexError, TypeError) as e:
        print(f"  ⚠️  [{fname}] traits 추출 실패: {e}")
        return None, {}


def compare_traits(all_traits_data):
    """
    모든 파일의 traits 키와 메타 필드 값이 동일한지 비교
    반환: 리포트 딕셔너리
    """
    # 1) 각 파일의 trait 키 목록 수집
    trait_keys_per_file = {}
    for fname, (breed_key, traits) in all_traits_data.items():
        trait_keys_per_file[fname] = set(traits.keys())

    all_trait_keys = set()
    for keys in trait_keys_per_file.values():
        all_trait_keys.update(keys)

    # 2) trait 키별로 메타 필드 값 수집
    # structure: { trait_key: { meta_field: { value: [파일명, ...] } } }
    trait_meta_values = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for fname, (breed_key, traits) in all_traits_data.items():
        for trait_key in all_trait_keys:
            if trait_key in traits:
                trait_obj = traits[trait_key]
                for mf in META_FIELDS:
                    val = trait_obj.get(mf, "__MISSING__")
                    trait_meta_values[trait_key][mf][str(val)].append(fname)
            else:
                trait_meta_values[trait_key]["__존재여부__"]["없음"].append(fname)

    return trait_keys_per_file, all_trait_keys, trait_meta_values


def print_report(trait_keys_per_file, all_trait_keys, trait_meta_values, all_files):
    n = len(all_files)
    print("\n" + "="*70)
    print(f"  검사 대상 파일 수: {n}개")
    print("="*70)

    # --- 1. trait 키 목록 일치 여부 ---
    print("\n[1] 각 파일의 trait 항목 목록 비교")
    all_same_keys = all(keys == list(trait_keys_per_file.values())[0]
                        for keys in trait_keys_per_file.values())
    if all_same_keys:
        print(f"  ✅ 모든 파일에 동일한 {len(all_trait_keys)}개 trait 항목이 있습니다.")
        print(f"     항목 목록: {sorted(all_trait_keys)}")
    else:
        print("  ❌ 파일마다 trait 항목 목록이 다릅니다!")
        for fname, keys in trait_keys_per_file.items():
            missing = all_trait_keys - keys
            extra = keys - all_trait_keys
            if missing or extra:
                print(f"     [{fname}]")
                if missing:
                    print(f"       없는 항목: {missing}")

    # --- 2. 각 trait의 메타 필드 값 일치 여부 ---
    print("\n[2] 각 trait 항목의 메타 필드 값 비교")
    inconsistencies_found = False

    for trait_key in sorted(all_trait_keys):
        trait_issues = []
        for mf in META_FIELDS:
            value_map = trait_meta_values[trait_key][mf]
            if len(value_map) > 1:
                # 값이 2개 이상 → 불일치
                trait_issues.append((mf, value_map))

        # 존재 여부 문제
        exist_issue = trait_meta_values[trait_key].get("__존재여부__", {})
        if exist_issue:
            trait_issues.append(("__존재여부__", exist_issue))

        if trait_issues:
            inconsistencies_found = True
            print(f"\n  ❌ [{trait_key}] — 불일치 발견:")
            for mf, value_map in trait_issues:
                print(f"     필드 '{mf}':")
                for val, fnames in value_map.items():
                    short_fnames = ", ".join(fnames[:5])
                    if len(fnames) > 5:
                        short_fnames += f" 외 {len(fnames)-5}개"
                    print(f"       값 '{val[:80]}' → {short_fnames}")
        else:
            print(f"  ✅ [{trait_key}] 모든 파일에서 동일")

    if not inconsistencies_found:
        print("\n  🎉 모든 trait 항목의 메타 필드가 전 파일에서 완전히 동일합니다!")

    # --- 3. score 값 분포 (참고용) ---
    print("\n[3] score 값 분포 (파일별 차이 있음 — 참고용)")
    print("  (score는 견종마다 달라야 정상이므로 불일치로 처리하지 않음)")
    for trait_key in sorted(all_trait_keys):
        scores = defaultdict(list)
        for fname, (breed_key, traits) in all_traits_data_global.items():
            if trait_key in traits:
                score = traits[trait_key].get("score", "N/A")
                scores[score].append(fname)
        score_summary = {k: len(v) for k, v in sorted(scores.items())}
        print(f"  [{trait_key}]: {score_summary}")

    print("\n" + "="*70)
    print("  검사 완료")
    print("="*70 + "\n")


# 전역 변수 (print_report에서 접근용)
all_traits_data_global = {}


def main():
    parser = argparse.ArgumentParser(description="견종 JSON traits 일관성 검사")
    parser.add_argument("--folder", default=".", help="JSON 파일 폴더 경로 (기본: 현재 폴더)")
    args = parser.parse_args()

    folder = args.folder
    print(f"\n📂 폴더 '{folder}'에서 JSON 파일 로드 중...")

    files = load_json_files(folder)
    if not files:
        print("  JSON 파일이 없습니다.")
        return

    print(f"  {len(files)}개 파일 로드 완료: {list(files.keys())}")

    # traits 추출
    global all_traits_data_global
    all_traits_data = {}
    for fname, data in files.items():
        breed_key, traits = extract_traits(data, fname)
        if breed_key:
            all_traits_data[fname] = (breed_key, traits)
    all_traits_data_global = all_traits_data

    if not all_traits_data:
        print("  traits 데이터를 추출할 수 없습니다.")
        return

    trait_keys_per_file, all_trait_keys, trait_meta_values = compare_traits(all_traits_data)
    print_report(trait_keys_per_file, all_trait_keys, trait_meta_values, files)


if __name__ == "__main__":
    main()