import os
import requests

# API 주소 설정
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/1000"

def get_recipe(menu_name):
    """ API에서 해당 메뉴의 레시피를 가져옴 """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()["COOKRCP01"]["row"]
        for menu in data:
            if menu["RCP_NM"] == menu_name:
                return {key: value for key, value in menu.items() if key.startswith("MANUAL")}
    return None

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
ingredient_file_path = os.path.join(data_dir, "ingredient.txt")

# ✅ `ingredient.txt`에서 메뉴명 읽기
if not os.path.exists(ingredient_file_path):
    print("❌ 식재료 정보 파일이 존재하지 않습니다.")
    exit()

with open(ingredient_file_path, "r", encoding="utf-8") as f:
    menu_name = f.readline().strip()  # 첫 번째 줄은 메뉴명

# ✅ API에서 레시피 가져오기
recipe_steps = get_recipe(menu_name)

if not recipe_steps:
    print(f"\n❌ '{menu_name}'의 레시피를 API에서 찾을 수 없습니다.")
    exit()

# ✅ 레시피 출력 (사용자가 Enter 키를 누르면 다음 단계로 이동)
print(f"\n🍽️ 선택한 메뉴: {menu_name}\n")
print("📜 레시피 단계별 안내:")
for i, step in sorted(recipe_steps.items()):
    if not step.strip():  # ✅ 값이 비어 있으면 즉시 종료
        break
    input(f"\n🔹 {step}\n👉 다음 단계로 진행하려면 Enter 키를 누르세요...")

# ✅ 모든 단계 완료 후 메시지 출력
print("\n🎉 모든 과정이 완료되었습니다! 맛있게 드세요! 🍽️")