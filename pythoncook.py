import os
import subprocess

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")
data_dir = os.path.join(base_dir, "data")  # ✅ `..` 제거하여 경로 수정

# ✅ `data/` 폴더가 없으면 자동 생성
if not os.path.exists(data_dir):
    print("⚠️ 'data' 폴더가 존재하지 않아 새로 생성합니다...")
    os.makedirs(data_dir, exist_ok=True)

# 사용자 입력 받기 (올바른 숫자 입력할 때까지 반복)
choice = None
while choice not in ["1", "2", "3"]:
    print("\n원하는 레시피 유형을 선택하세요:")
    print("1. 유형에 따른 레시피\n2. 보유 재료에 따른 레시피\n3. 음식 종류에 따른 레시피")
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

# ✅ 실행이 끝난 후 파일 초기화 기능 추가
input("\n✅ 모든 과정이 종료되었습니다. 종료하시려면 Enter 키를 누르세요...")

# ✅ `data/` 폴더 내 모든 `.txt` 및 `.jpg` 파일을 빈 파일로 초기화
for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    if file_name.endswith(".txt") or file_name.endswith(".jpg"):
        open(file_path, "w").close()  # ✅ 파일 내용을 비우기
       