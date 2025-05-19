import requests
import json
import os

# API URL
url = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/100"
menu_file = "menu_list.txt"
selection_file = "selected_menu.txt"

# 파일 존재 여부 확인
if not os.path.exists(menu_file) or os.stat(menu_file).st_size == 0:
    print("\n❌ 오류: 메뉴 데이터가 없습니다. 'menu_selection.py'를 먼저 실행해 주세요.")
    exit()

# menu_selection.py에서 생성된 메뉴 파일 읽기
with open(menu_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 선택 가능한 메뉴 목록 가져오기
menu_dict = {}
for line in lines[1:]:  # 첫 줄 제외
    parts = line.split(". ")  # 번호와 메뉴명 분리
    if len(parts) > 1:
        menu_dict[parts[0].strip()] = parts[1].strip()  # {"99": "콩고기샐러드"}

# 유저 입력 반복 처리
while True:
    print("\n선택한 메뉴의 번호를 입력하세요. 하나만 선택 가능합니다.")
    choice = input("예: 1\n입력: ")

    if choice in menu_dict:
        selected_menu = menu_dict[choice]  # 번호를 기반으로 메뉴명 가져오기
        break
    else:
        print(f"❌ '{choice}'번 메뉴는 존재하지 않습니다. 다시 선택하세요.")

# API 데이터 가져오기
response = requests.get(url)
data = response.json()

# 선택한 메뉴의 인덱스를 기반으로 API에서 재료 가져오기
index = int(choice) - 1  # API의 인덱스와 맞추기
selected_recipe = data['COOKRCP01']['row'][index]
ingredient_list = selected_recipe['RCP_PARTS_DTLS']

# ✅ 재료 정보가 여러 줄일 경우 올바르게 저장
formatted_ingredients = ingredient_list.replace("\r", "").replace("\n", ", ")  # 줄바꿈을 쉼표로 변환

# ✅ 메뉴명과 전체 재료 정보를 함께 저장
with open(selection_file, "w", encoding="utf-8") as f:
    f.write(f"{selected_recipe['RCP_NM']}\n{formatted_ingredients}\n")
