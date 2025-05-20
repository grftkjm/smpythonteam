import os
import requests

# API 주소 설정
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/100"

def get_menu_data():
    """ API에서 메뉴 데이터를 가져옴 """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data["COOKRCP01"]["row"]  # API 데이터에서 메뉴 목록을 추출
    else:
        raise Exception("❌ API에서 데이터를 불러오는 데 실패했습니다.")

def filter_menu_by_ingredient(menu_data, ingredient):
    """ 사용자가 입력한 식재료를 포함하는 메뉴 필터링 """
    filtered_menu = []

    for i, menu in enumerate(menu_data):
        try:
            menu_name = f"{i+1}. {menu['RCP_NM']} ({menu['INFO_ENG']} kcal)"
            ingredients = menu["RCP_PARTS_DTLS"]

            if ingredient in ingredients:
                filtered_menu.append(menu_name)
        except ValueError:
            pass  # 식재료 정보가 없거나 잘못된 경우 무시

    return filtered_menu

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# 'data' 폴더가 없으면 생성
os.makedirs(data_dir, exist_ok=True)

# 사용자 입력 받기
ingredient = input("보유중인 식재료를 입력하세요: ").strip()

# API에서 메뉴 데이터 가져오기
menu_data = get_menu_data()
filtered_menu = filter_menu_by_ingredient(menu_data, ingredient)

# ✅ 필터링된 메뉴가 없으면 경고 메시지 출력
if not filtered_menu:
    print(f"\n⚠️ '{ingredient}'을(를) 포함하는 메뉴를 찾을 수 없습니다.")
else:
    # ✅ 필터링된 메뉴 목록 저장
    menu_file_path = os.path.join(data_dir, "menu_list.txt")
    with open(menu_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_menu))

    # 결과 출력
    print("\n✅ 추천 메뉴 목록:")
    for menu in filtered_menu:
        print(menu)

   