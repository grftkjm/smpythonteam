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

def calculate_tdee(weight, height, age, gender, activity_level):
    """ 사용자의 정보를 바탕으로 TDEE 계산 """
    if gender.lower() == "남성":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:  # 여성
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    activity_factor = {
        "1": 1.2,  # 운동 거의 안함
        "2": 1.375,  # 가벼운 운동 (주 1~3회)
        "3": 1.55,  # 중간 정도 운동 (주 3~5회)
        "4": 1.725,  # 고강도 운동 (주 6~7회)
        "5": 1.9   # 아주 높은 운동량 (운동선수 수준)
    }

    return bmr * activity_factor.get(activity_level, 1.2)  # 기본값 1.2(거의 운동 안 함)

def filter_menu(menu_data, choice, tdee=None, calorie_deficit=0):
    """ 사용자의 선택에 맞게 메뉴 필터링 """
    filtered_menu = []

    if choice in ["다이어트식", "밥과 함께 먹을 다이어트식"]:
        target_calories = (tdee - calorie_deficit) / 3
        if choice == "밥과 함께 먹을 다이어트식":
            target_calories -= 300
    else:
        target_calories = None  # 일반식의 경우 제한 없이 전체 메뉴 출력

    for i, menu in enumerate(menu_data):
        try:
            menu_name = f"{i+1}. {menu['RCP_NM']} ({menu['INFO_ENG']} kcal)"
            menu_calories = float(menu["INFO_ENG"])

            if target_calories is None or menu_calories <= target_calories:
                filtered_menu.append(menu_name)
        except ValueError:
            pass  # 칼로리 값이 없거나 잘못된 경우 무시

    return filtered_menu

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# 'data' 폴더가 없으면 생성
os.makedirs(data_dir, exist_ok=True)

# 사용자 입력 받기 (올바른 숫자 입력할 때까지 반복)
choice = None
while choice not in ["1", "2", "3"]:
    print("\n메뉴 유형을 선택하세요:")
    print("1. 일반식\n2. 밥과 함께 먹을 다이어트식\n3. 다이어트식")
    choice = input("번호 입력: ").strip()

    if choice not in ["1", "2", "3"]:
        print("❌ 올바른 숫자를 입력하세요. (1~3 중 선택)")

# 선택한 옵션 설정
choice_map = {
    "1": "일반식",
    "2": "밥과 함께 먹을 다이어트식",
    "3": "다이어트식"
}
choice = choice_map[choice]

# 다이어트식을 선택한 경우 TDEE 및 감량 목표 입력 요청
tdee = None
calorie_deficit = 0

if choice in ["다이어트식", "밥과 함께 먹을 다이어트식"]:
    print("\n🔹 TDEE를 계산하기 위해 다음 정보를 입력하세요.")
    weight = float(input("체중 (kg): "))
    height = float(input("키 (cm): "))
    age = int(input("나이: "))
    gender = input("성별 (남성/여성): ").strip().lower()
    
    print("\n🔹 운동 수준을 선택하세요:")
    print("1. 거의 운동 안 함\n2. 가벼운 운동 (주 1~3회)\n3. 중간 운동 (주 3~5회)\n4. 고강도 운동 (주 6~7회)\n5. 매우 높은 수준 운동 (운동선수)")
    activity_level = input("번호 입력: ").strip()

    tdee = calculate_tdee(weight, height, age, gender, activity_level)
    print(f"\n✅ 당신의 TDEE는 {tdee:.2f} kcal 입니다.")

    # 일주일 감량 목표 입력
    weight_loss_goal = float(input("\n🔹 일주일 목표 감량량 (kg): "))
    
    if weight_loss_goal > 1.5:
        print("\n⚠️ 건강한 다이어트를 위해 일주일 1.5kg을 초과하는 감량은 권장되지 않습니다.")
        print("✅ 1.5kg 기준으로 추천해드릴게요.")
        weight_loss_goal = 1.5  # 최대 1.5kg으로 제한
    
    calorie_deficit = (weight_loss_goal * 7700) / 7  # 하루 감량 목표 칼로리
    print(f"\n✅ 일주일 목표 감량량: {weight_loss_goal}kg")
    print(f"🔻 하루 줄여야 할 칼로리: {calorie_deficit:.2f} kcal")

# API에서 메뉴 데이터 가져오기
menu_data = get_menu_data()
filtered_menu = filter_menu(menu_data, choice, tdee, calorie_deficit)

# ✅ 필터링된 메뉴가 없으면 일반식으로 변경
if not filtered_menu and choice in ["다이어트식", "밥과 함께 먹을 다이어트식"]:
    print("\n⚠️ 사용자의 신체에 비해 과한 체중감량 목표입니다. 일반식과 적절한 운동을 통한 다이어트를 권장합니다.")
    choice = "일반식"
    time.sleep(5)  # 5초 대기 후 일반식 출력
    filtered_menu = filter_menu(menu_data, choice)  # 일반식으로 변경하여 필터링

# ✅ 선택한 옵션 저장
option_file_path = os.path.join(data_dir, "selected_option.txt")
with open(option_file_path, "w", encoding="utf-8") as f:
    f.write(choice)

# ✅ 필터링된 메뉴 목록 저장
menu_file_path = os.path.join(data_dir, "menu_list.txt")
with open(menu_file_path, "w", encoding="utf-8") as f:
    f.write("\n".join(filtered_menu))

# 결과 출력
print("\n✅ 추천 메뉴 목록:")
for menu in filtered_menu:
    print(menu)

print(f"\n📁 메뉴 데이터가 '{menu_file_path}'에 저장되었습니다!")