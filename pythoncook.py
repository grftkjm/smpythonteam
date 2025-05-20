import os
import subprocess

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")

# 사용자 입력 받기 (올바른 숫자 입력할 때까지 반복)
choice = None
while choice not in ["1", "2", "3"]:
    print("\n원하는 레시피 유형을 선택하세요:")
    print("1. 다이어트를 위한 레시피\n2. 보유 재료에 따른 레시피\n3. 음식 종류에 따른 레시피")
    choice = input("번호 입력: ").strip()

    if choice not in ["1", "2", "3"]:
        print("❌ 올바른 숫자를 입력하세요. (1~3 중 선택)")

# 실행할 파일 목록 설정
if choice == "1":
    scripts = ["option_select.py", "menu_select.py", "ingredient_display.py"]
elif choice == "2":
    scripts = ["ingredient_select.py", "menu_select.py", "ingredient_display.py"]
else:
    scripts = ["type_select.py", "menu_select.py", "ingredient_display.py"]  # ✅ 음식 종류 선택 추가

# 각 단계 실행
for script in scripts:
    script_path = os.path.join(src_dir, script)
    subprocess.run(["python", script_path])

# ✅ `ingredient_display.py`가 끝난 후 레시피 안내 질문 추가
recipe_choice = input("\n🍽️ 해당하는 레시피를 알려드릴까요? (예/아니오): ").strip().lower()

if recipe_choice in ["예", "y"]:
    recipe_path = os.path.join(src_dir, "recipe.py")
    subprocess.run(["python", recipe_path])

# ✅ 실행이 끝난 후 종료 방지 메시지 추가
input("\n✅ 모든 과정이 종료되었습니다. 종료하시려면 Enter 키를 누르세요...")