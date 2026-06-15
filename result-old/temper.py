import json
import glob
import os

def extract_alert_breeds(json_dir: str = ".") -> dict[str, str]:
    """temperament에 'Alert'가 포함된 견종과 temperament를 반환"""
    alert_breeds = {}
    
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    
    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        traits = (
            data
            .get("settings", {})
            .get("breed_data", {})
            .get("traits", {})
        )
        
        for breed, breed_data in traits.items():
            temperament = breed_data.get("temperament", "")
            keywords = [kw.strip() for kw in temperament.split("/")]
            
            if "Alert" in keywords:
                breed_name = breed_data.get("breed_name", breed)
                alert_breeds[breed_name] = temperament
    
    return alert_breeds


if __name__ == "__main__":
    json_dir = "."
    
    alert_breeds = extract_alert_breeds(json_dir)
    
    print(f"Alert 기질 견종: {len(alert_breeds)}개\n")
    
    lines = []
    for breed_name, temperament in sorted(alert_breeds.items()):
        line = f"{breed_name} ({temperament})"
        print(line)
        lines.append(line)
    
    with open("alert_breeds.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n'alert_breeds.txt'에 저장 완료")
