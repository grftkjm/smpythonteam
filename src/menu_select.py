import os
import requests

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
menu_file_path = os.path.join(data_dir, "menu_list.txt")
ingredient_file_path = os.path.join(data_dir, "ingredient.txt")

# API 주소 설정
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

def get_menu_data():
    """ API에서 메뉴 데이터를 가져옴 """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data["COOKRCP01"]["row"]  # API 데이터에서 메뉴 목록을 추출
    else:
        raise Exception("❌ API에서 데이터를 불러오는 데 실패했습니다.")

# API에서 메뉴 데이터 가져오기
menu_data = get_menu_data()

# ✅ `menu_list.txt`에서 메뉴 목록 읽기
if not os.path.exists(menu_file_path):
    print("❌ 메뉴 리스트 파일이 존재하지 않습니다.")
    exit()

with open(menu_file_path, "r", encoding="utf-8") as f:
    menu_list = [line.strip() for line in f.readlines()]

# ✅ 메뉴 번호 입력 및 검증
while True:
    print("\n✅ 추천 메뉴 목록:")
    for menu in menu_list:
        print(menu)

    selected_number = input("\n원하는 메뉴 번호를 입력하세요: ").strip()

    # 입력한 번호가 `menu_list.txt`에 존재하는지 확인
    valid_numbers = [menu.split(".")[0] for menu in menu_list]

    if selected_number in valid_numbers:
        break
    else:
        print("❌ 올바른 번호를 입력하세요.")

# ✅ 입력한 번호에 해당하는 메뉴 찾기
selected_menu = next(menu for menu in menu_list if menu.startswith(f"{selected_number}."))
menu_name = selected_menu.split(". ")[1].split(" (")[0]

# ✅ API 데이터에서 해당 메뉴 찾기
menu_info = next((menu for menu in menu_data if menu["RCP_NM"] == menu_name), None)

if not menu_info:
    print(f"\n❌ '{menu_name}'의 정보를 API에서 찾을 수 없습니다.")
    exit()

# ✅ 선택한 메뉴의 식재료 저장
ingredients = menu_info["RCP_PARTS_DTLS"]
with open(ingredient_file_path, "w", encoding="utf-8") as f:
    f.write(f"{menu_name}\n{ingredients}")
