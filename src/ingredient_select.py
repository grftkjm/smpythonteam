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

def filter_menu_by_ingredient(menu_data, ingredient):
    """ 사용자가 입력한 식재료를 포함하는 메뉴 필터링 """
    filtered_menu = [menu for menu in menu_data if ingredient in menu.get("RCP_PARTS_DTLS", "")]

    return filtered_menu

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
os.makedirs(data_dir, exist_ok=True)

# API에서 메뉴 데이터 가져오기
menu_data = get_menu_data()

# ✅ **식재료 입력 및 검증 로직 추가**
while True:
    ingredient = input("보유한 식재료를 입력하세요: ").strip()
    
    # 입력한 식재료가 API 내의 메뉴 재료에 포함되어 있는지 확인
    filtered_menu = filter_menu_by_ingredient(menu_data, ingredient)

    if filtered_menu:
        break  # 유효한 식재료 입력 시 반복 종료
    else:
        print(f"\n⚠️ '{ingredient}'을(를) 포함하는 메뉴를 찾을 수 없습니다. 다시 입력해주세요.")

# ✅ **필터링된 메뉴 리스트 저장**
menu_file_path = os.path.join(data_dir, "menu_list.txt")
with open(menu_file_path, "w", encoding="utf-8") as f:
    for i, menu in enumerate(filtered_menu, 1):
        f.write(f"{i}. {menu['RCP_NM']} ({menu['INFO_ENG']} kcal)\n")



