def calculate_bmr(weight, height, age, gender):
    """ 기초대사량(BMR) 계산 (해리스-베네딕트 공식) """
    gender = gender.lower()
    if gender == "남자":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender == "여자":
        return (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        raise ValueError("성별은 '남자' 또는 '여자'로 입력해야 합니다.")

def calculate_tdee(bmr, activity_level):
    """ 총에너지소비량(TDEE) 계산 """
    activity_factors = {
        "거의 활동 없음": 1.2,
        "가벼운 운동": 1.375,
        "규칙적 운동": 1.55,
        "고강도 운동": 1.725,
        "운동선수 수준": 1.9
    }
    return bmr * activity_factors.get(activity_level, 1.2)

# 사용자 입력 받기
weight = float(input("체중(kg): "))
height = float(input("키(cm): "))
age = int(input("나이: "))
gender = input("성별 (남자/여자): ").strip()

print("\n활동 수준을 선택하세요:")
print("1. 거의 활동 없음\n2. 가벼운 운동\n3. 규칙적 운동\n4. 고강도 운동\n5. 운동선수 수준")
activity_choice = input("번호 입력: ")

activity_levels = {
    "1": "거의 활동 없음",
    "2": "가벼운 운동",
    "3": "규칙적 운동",
    "4": "고강도 운동",
    "5": "운동선수 수준"
}
activity_level = activity_levels.get(activity_choice, "거의 활동 없음")

# BMR 및 TDEE 계산
bmr = calculate_bmr(weight, height, age, gender)
tdee = calculate_tdee(bmr, activity_level)

# ✅ TDEE 값을 파일에 저장
with open("tdee_info.txt", "w", encoding="utf-8") as f:
    f.write(str(tdee))

# 결과 출력
print(f"\n✅ 당신의 BMR(기초대사량): {bmr:.2f} kcal")
print(f"✅ 당신의 TDEE(총에너지소비량, {activity_level} 기준): {tdee:.2f} kcal")