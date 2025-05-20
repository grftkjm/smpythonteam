import os
import subprocess

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")

# 사용자 입력 받기 (올바른 숫자 입력할 때까지 반복)
choice = None
while choice not in ["1", "2"]:
    print("\n원하는 레시피 유형을 선택하세요:")
    print("1. 유형에 따른 레시피\n2. 보유 재료에 따른 레시피")
    choice = input("번호 입력: ").strip()

    if choice not in ["1", "2"]:
        print("❌ 올바른 숫자를 입력하세요. (1 또는 2 중 선택)")

# 실행할 파일 목록 설정
if choice == "1":
    scripts = ["option_select.py", "menu_select.py", "ingredient_display.py"]
else:
    scripts = ["ingredient_select.py", "menu_select.py", "ingredient_display.py"]  # ✅ ingredient_select.py로 변경

# 각 단계 실행
for script in scripts:
    script_path = os.path.join(src_dir, script)
    subprocess.run(["python", script_path])