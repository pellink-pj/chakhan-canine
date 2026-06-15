import json
import glob
import os

def extract_temperament_keywords(json_dir: str = ".") -> set[str]:
    """
    여러 JSON 파일에서 temperament 키워드를 추출하고 중복 제거하여 반환
    """
    keywords = set()
    
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    print(f"발견된 JSON 파일: {len(json_files)}개")
    
    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # settings > breed_data > traits 경로 탐색
        traits = (
            data
            .get("settings", {})
            .get("breed_data", {})
            .get("traits", {})
        )
        
        for breed, breed_data in traits.items():
            temperament = breed_data.get("temperament", "")
            if temperament:
                # " / " 또는 "/" 기준으로 분리, 공백 정리
                parts = [kw.strip() for kw in temperament.split("/")]
                keywords.update(p for p in parts if p)
    
    return keywords


if __name__ == "__main__":
    # JSON 파일들이 있는 디렉토리 경로 지정
    json_dir = "."  # 필요시 변경
    
    all_keywords = extract_temperament_keywords(json_dir)
    
    print(f"\n총 고유 키워드: {len(all_keywords)}개")
    print("\n--- Temperament 키워드 목록 ---")
    for kw in sorted(all_keywords):
        print(kw)
    
    # 결과를 텍스트 파일로 저장
    output_path = "temperament_keywords.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(all_keywords)))
    print(f"\n'{output_path}'에 저장 완료")
