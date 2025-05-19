import os

# 프로젝트 폴더 구조 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")

# `ingredient.txt` 파일 경로
ingredient_file_path = os.path.join(data_dir, "ingredient.txt")

# 파일 존재 여부 확인
if not os.path.exists(ingredient_file_path):
    print("❌ ingredient.txt 파일을 찾을 수 없습니다. 먼저 menu_select.py를 실행하세요.")
    exit()

# 파일 읽기 및 출력
with open(ingredient_file_path, "r", encoding="utf-8") as f:
    content = f.read().strip()

if not content:
    print("❌ ingredient.txt 파일이 비어 있습니다. 먼저 menu_select.py를 실행하여 데이터를 저장하세요.")
    exit()

# 결과 출력
print("\n📋 선택한 메뉴와 식재료 목록:")
print(content)