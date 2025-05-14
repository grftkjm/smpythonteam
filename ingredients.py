import requests

# API 키 및 URL 설정
API_Key = "7904b29570d44de38aa6"
URL = f"http://openapi.foodsafetykorea.go.kr/api/{API_Key}/COOKRCP01/json/1/100"

# API 요청 및 JSON 데이터 변환
response = requests.get(URL)
data = response.json()

# 'COOKRCP01'에서 레시피 목록 가져오기
recipes = data.get("COOKRCP01", {}).get("row", [])

# 저장된 메뉴 이름 불러오기
try:
    with open("selected_recipe.txt", "r", encoding="utf-8") as f:
        selected_recipe_name = f.read().strip()

    # 선택된 메뉴에 해당하는 레시피 검색
    selected_recipe = next((recipe for recipe in recipes if recipe["RCP_NM"] == selected_recipe_name), None)

    if selected_recipe:
        print(f"\n{selected_recipe_name}의 재료 목록:\n{selected_recipe['RCP_PARTS_DTLS']}")
    else:
        print("선택된 메뉴를 찾을 수 없습니다.")
except FileNotFoundError:
    print("선택된 메뉴 파일이 없습니다! 먼저 menu.py를 실행하세요.")