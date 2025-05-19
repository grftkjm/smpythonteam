import os

def calculate_bmr(weight, height, age, gender):
    """ 기초대사량(BMR) 계산 """
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

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# 'data' 폴더가 없으면 생성
os.makedirs(data_dir, exist_ok=True)

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

# ✅ 일주일 목표 다이어트량 입력
target_loss_kg = float(input("\n일주일 목표 다이어트량을 kg 단위로 입력하세요 (ex: 0.5): "))

# 최대 감량 제한 (1.5kg)
if target_loss_kg > 1.5:
    print("⚠️ 건강한 감량을 위해 일주일 최대 감량을 1.5kg로 제한합니다.")
    target_loss_kg = 1.5

calories_to_cut_per_day = (target_loss_kg * 7700) / 7  # 체중 1kg 감량을 위한 7700kcal 기준

# 조정된 TDEE 계산
adjusted_tdee = max(tdee - calories_to_cut_per_day, 0)  # 최소 0kcal 이상 유지

# ✅ 수정된 경로로 TDEE 값을 파일에 저장
tdee_file_path = os.path.join(data_dir, "tdee_info.txt")
with open(tdee_file_path, "w", encoding="utf-8") as f:
    f.write(str(adjusted_tdee))

# 결과 출력
print(f"\n✅ 당신의 BMR(기초대사량): {bmr:.2f} kcal")
print(f"✅ 당신의 TDEE(총에너지소비량, {activity_level} 기준): {tdee:.2f} kcal")
print(f"✅ 목표 감량 {target_loss_kg:.2f}kg을 위해 하루 {adjusted_tdee:.2f} kcal 이하로 섭취해야 합니다.")
