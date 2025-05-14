import subprocess

# menu.py 실행
print("🔹 메뉴 선택 중...")
subprocess.run(["python", "menu.py"], check=True)

# 선택한 메뉴 이름 가져오기
try:
    with open("selected_recipe.txt", "r", encoding="utf-8") as f:
        selected_recipe_name = f.read().strip()
    print(f"\n🔹 '{selected_recipe_name}'의 재료 불러오는 중...")
except FileNotFoundError:
    print("\n🔹 선택한 메뉴를 찾을 수 없습니다.")
    exit()

# ingredients.py 실행
subprocess.run(["python", "ingredients.py"], check=True)