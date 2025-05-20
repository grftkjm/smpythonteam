import os
import requests

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

def filter_menu_by_category(menu_data, category):
    """ 사용자가 선택한 카테고리에 해당하는 메뉴 필터링 """
    filtered_menu = [menu for menu in menu_data if category in menu.get("RCP_PAT2", "")]

    return filtered_menu

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# ✅ 메뉴 유형 선택 (올바른 숫자 입력할 때까지 반복)
category_map = {
    "1": "국&찌개",
    "2": "반찬",
    "3": "일품",
    "4": "후식"
}

category_choice = None
while category_choice not in category_map:
    print("\n✅ 원하는 메뉴 유형을 선택하세요:")
    print("1. 국&찌개\n2. 반찬\n3. 일품(밥대용)\n4. 후식")
    category_choice = input("번호 입력: ").strip()

    if category_choice not in category_map:
        print("❌ 올바른 번호를 입력하세요. (1~4 중 선택)")

category = category_map[category_choice]

# ✅ API에서 메뉴 데이터 가져오기
menu_data = get_menu_data()
filtered_menu = filter_menu_by_category(menu_data, category)

# ✅ 필터링된 메뉴가 없으면 경고 메시지 출력
if not filtered_menu:
    print(f"\n⚠️ '{category}' 카테고리에 해당하는 메뉴를 찾을 수 없습니다.")
else:
    # ✅ 필터링된 메뉴 목록 저장
    menu_file_path = os.path.join(data_dir, "menu_list.txt")
    with open(menu_file_path, "w", encoding="utf-8") as f:
        for i, menu in enumerate(filtered_menu, 1):
            f.write(f"{i}. {menu['RCP_NM']} ({menu['INFO_ENG']} kcal)\n")

  

