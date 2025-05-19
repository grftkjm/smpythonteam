import os
import time
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

def filter_menu(menu_data, tdee, choice):
    """ 사용자의 선택에 맞게 메뉴 필터링 """
    filtered_menu = []
    diet_calories = tdee / 3
    rice_adjusted_calories = diet_calories - 300

    # 밥과 함께 먹을 다이어트식 선택 시 권장 칼로리 초과 확인
    if choice == "밥과 함께 먹을 다이어트식" and rice_adjusted_calories < 0:
        print("\n⚠️ 밥 한 공기의 칼로리(약 300 kcal)가 다이어트 권장 열량을 초과합니다. 일반 다이어트식을 추천합니다.")
        choice = "다이어트식"

    for i, menu in enumerate(menu_data):
        try:
            menu_name = f"{i+1}. {menu['RCP_NM']} ({menu['INFO_ENG']} kcal)"
            menu_calories = float(menu["INFO_ENG"])

            if choice == "상관없음":
                filtered_menu.append(menu_name)
            elif choice == "밥과 함께 먹을 다이어트식" and menu_calories <= rice_adjusted_calories:
                filtered_menu.append(menu_name)
            elif choice == "다이어트식" and menu_calories <= diet_calories:
                filtered_menu.append(menu_name)
            elif choice == "일반식" and menu_calories >= diet_calories:
                filtered_menu.append(menu_name)
        except ValueError:
            pass  # 칼로리 값이 없거나 잘못된 경우 무시

    # 밥과 함께 먹을 다이어트식을 선택했지만 해당하는 음식이 없을 경우 자동 변경
    if choice == "밥과 함께 먹을 다이어트식" and not filtered_menu:
        print("\n⚠️ 밥과 함께 먹을 다이어트식 기준에 맞는 음식이 없습니다. 일반 다이어트식을 추천합니다.")
        choice = "다이어트식"
        filtered_menu, _, _ = filter_menu(menu_data, tdee, choice)

    # 다이어트식을 선택했지만 해당하는 음식이 없을 경우 자동 변경
    if choice == "다이어트식" and not filtered_menu:
        print("\n⚠️ 다이어트 권장 열량 이하의 음식이 없습니다. 일반식과 함께 적절한 운동을 권장합니다.")
        choice = "일반식"
        filtered_menu, _, _ = filter_menu(menu_data, tdee, choice)

    return filtered_menu, choice

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# 'data' 폴더가 없으면 생성
os.makedirs(data_dir, exist_ok=True)

# 사용자 입력 받기
print("메뉴 유형을 선택하세요:")
print("1. 일반식\n2. 밥과 함께 먹을 다이어트식\n3. 다이어트식\n4. 상관없음")
choice_map = {
    "1": "일반식",
    "2": "밥과 함께 먹을 다이어트식",
    "3": "다이어트식",
    "4": "상관없음"
}
choice = choice_map.get(input("번호 입력: "), "상관없음")

tdee_file_path = os.path.join(data_dir, "tdee_info.txt")

# TDEE 값 불러오기
try:
    with open(tdee_file_path, "r", encoding="utf-8") as f:
        tdee = float(f.read().strip())
except FileNotFoundError:
    print("❌ TDEE 값을 찾을 수 없습니다. 먼저 TDEE.py를 실행하세요.")
    exit()

# API에서 메뉴 데이터를 가져옴
menu_data = get_menu_data()
filtered_menu, final_choice = filter_menu(menu_data, tdee, choice)

# 특정 선택지일 경우 메시지 출력 후 5초 대기
if final_choice == "밥과 함께 먹을 다이어트식":
    print(f"\n사용자의 신체에 맞는 다이어트 권장 열량에서 밥 한 공기의 칼로리(300 kcal)를 제외한 칼로리는 {tdee/3 - 300:.2f} kcal 입니다.")
    print("해당 열량 이하의 음식 불러오는 중...")
    time.sleep(5)
elif final_choice == "다이어트식":
    print(f"\n사용자의 신체에 맞는 다이어트 권장 칼로리는 {tdee/3:.2f} kcal 입니다.")
    print("해당 열량 이하의 음식 불러오는 중...")
    time.sleep(5)

# 메뉴 목록을 파일에 저장
menu_file_path = os.path.join(data_dir, "menu_list.txt")
with open(menu_file_path, "w", encoding="utf-8") as f:
    f.write("\n".join(filtered_menu))

# 결과 출력
print("\n✅ 추천 메뉴 목록:")
for menu in filtered_menu:
    print(menu)
