import os

# 파일 경로
selection_file = "selected_menu.txt"

# 파일 존재 여부 확인
if not os.path.exists(selection_file) or os.stat(selection_file).st_size == 0:
    print("\n❌ 오류: 선택한 메뉴 정보가 없습니다. 'menu_save.py'를 먼저 실행해 주세요.")
    exit()

# 선택한 메뉴 불러오기
with open(selection_file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    selected_menu = lines[0].strip()  # 메뉴명
    ingredient_list = lines[1].strip()  # 재료 정보

# 결과 출력
print(f"\n✅ '{selected_menu}'의 재료 목록:")
print(ingredient_list)