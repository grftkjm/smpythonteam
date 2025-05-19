import os
import requests

# API 주소 설정
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/100"

def get_recipe_details(menu_index):
    """ API에서 특정 번호에 해당하는 메뉴의 식재료 목록을 가져옴 """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        recipes = data["COOKRCP01"]["row"]

        # 입력받은 번호가 API 데이터의 인덱스 범위 내에 있는지 확인
        if 1 <= menu_index <= len(recipes):
            selected_recipe = recipes[menu_index - 1]  # API 데이터는 0부터 시작하므로 -1
            return selected_recipe["RCP_NM"], selected_recipe["RCP_PARTS_DTLS"]
    return None, None  # 메뉴가 없을 경우

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# 'data' 폴더가 없으면 생성
os.makedirs(data_dir, exist_ok=True)

# 메뉴 리스트 파일 경로
menu_file_path = os.path.join(data_dir, "menu_list.txt")

# 메뉴 리스트 불러오기
try:
    with open(menu_file_path, "r", encoding="utf-8") as f:
        menu_list = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print("❌ 메뉴 리스트 파일을 찾을 수 없습니다. 먼저 option_select.py를 실행하세요.")
    exit()

# 사용자 입력 받기 (올바른 메뉴 번호를 선택할 때까지 반복)
selected_menu = None
selected_index = None

while selected_menu is None:
    try:
        menu_choice = input("\n선택할 메뉴 번호를 입력하세요: ").strip()

        # 입력한 번호가 menu_list에 존재하는지 검증
        matched_menu = None
        for menu in menu_list:
            if menu.startswith(menu_choice + "."):
                matched_menu = menu
                break

        if not matched_menu:
            print("❌ 입력한 메뉴 번호가 존재하지 않습니다. 다시 입력하세요.")
            continue

        # 숫자 변환 후 API 데이터에서 검색
        menu_choice_int = int(menu_choice)
        selected_menu, ingredients = get_recipe_details(menu_choice_int)

        if not ingredients:
            print(f"❌ '{selected_menu}'에 대한 식재료 정보를 찾을 수 없습니다.")
            exit()

    except ValueError:
        print("❌ 숫자를 입력하세요.")

# ✅ 식재료 정보 저장 (ingredient.txt로 고정)
ingredient_file_path = os.path.join(data_dir, "ingredient.txt")
with open(ingredient_file_path, "w", encoding="utf-8") as f:
    f.write(f"메뉴명: {selected_menu}\n\n식재료:\n{ingredients}")

