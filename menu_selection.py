import os
import math
import re
import time  #  5초 대기 기능 추가

# 파일 경로
menu_file = "menu_list.txt"
tdee_file = "tdee_info.txt"

# 파일 존재 여부 확인
if not os.path.exists(menu_file) or os.stat(menu_file).st_size == 0:
    print("\n❌ 오류: 메뉴 데이터가 없습니다. 'menu_save.py'를 먼저 실행해 주세요.")
    exit()

if not os.path.exists(tdee_file) or os.stat(tdee_file).st_size == 0:
    print("\n❌ 오류: TDEE 데이터가 없습니다. 'TDEE.py'를 먼저 실행해 주세요.")
    exit()

# TDEE 값 불러오기
with open(tdee_file, "r", encoding="utf-8") as f:
    tdee = float(f.readline().strip())  # 저장된 TDEE 값 가져오기

adjusted_tdee = round((tdee - 700) / 3, 1)  #  소수 첫째 자리에서 반올림

# 음식 유형 선택
print("\n식사 유형을 선택하세요:")
print("1. 일반식\n2. 밥과 함께 먹을 다이어트식\n3. 밥 없이 먹을 다이어트식\n4. 상관없음")
choice = input("번호 입력: ")

# 선택한 유형에 맞게 칼로리 범위 설정
if choice == "1":
    calorie_limit = float('inf')  # 모든 메뉴 출력 (제한 없음)

elif choice == "2":
    calorie_limit = adjusted_tdee - 300  # 밥과 함께 먹을 경우 밥 칼로리 제외

    # ✅ 밥과 함께 먹을 다이어트식 선택 시, 추천 열량 출력 후 3초 대기
    print(f"\n🍚 사용자의 신체에 맞는 다이어트 칼로리에서 밥 한 공기 약 300kcal를 제외한 추천 열량은 {calorie_limit:.1f} kcal 이하 입니다.")
    print("⏳ 해당하는 열량의 메뉴를 불러오는 중...")
    time.sleep(5)  # 🚀 5초 대기 후 메뉴 출력

elif choice == "3":
    calorie_limit = adjusted_tdee  # 밥 없이 먹을 경우 TDEE ÷ 3 그대로 적용

    # ✅ 밥 없이 먹을 다이어트식 선택 시, 추천 열량 출력 후 3초 대기
    print(f"\n🥗 사용자의 신체에 맞는 다이어트 추천 열량은 {calorie_limit:.1f} kcal 이하 입니다.")
    print("⏳ 해당하는 열량의 메뉴를 불러오는 중...")
    time.sleep(5)  # 🚀 5초 대기 후 메뉴 출력

elif choice == "4":
    calorie_limit = None  # 상관없음 → 모든 다이어트식 + 일반식 출력

else:
    print("❌ 잘못된 입력입니다. 다시 실행해 주세요.")
    exit()

# 메뉴 파일 읽기 및 필터링
with open(menu_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

print("\n✅ 선택한 조건에 맞는 메뉴:")
for line in lines[1:]:  # 첫 줄(선택한 유형)을 제외하고 메뉴 출력
    parts = line.strip().split(" (")
    menu_name = parts[0]
    calorie_info = parts[1] if len(parts) > 1 else ""

    # 칼로리 추출 (정규 표현식 활용)
    kcal_value = None
    if "kcal" in calorie_info:
        match = re.search(r"\d+(\.\d+)?", calorie_info)  # 숫자(소수 포함)만 추출
        if match:
            kcal_value = float(match.group())  # 올바른 숫자 값으로 변환

    # 선택 유형에 따라 출력 결정
    if calorie_limit is None or kcal_value is None or kcal_value <= calorie_limit:
        print(f"- {menu_name} ({kcal_value:.1f} kcal)")

print("\n✅ 유형 선택을 완료했습니다.")