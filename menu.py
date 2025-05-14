import requests
import pandas as pd

# 출력 옵션 설정
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# API 키 및 URL 설정
API_Key = "7904b29570d44de38aa6"
URL = f"http://openapi.foodsafetykorea.go.kr/api/{API_Key}/COOKRCP01/json/1/100"

# API 요청 및 JSON 데이터 변환
response = requests.get(URL)
data = response.json()

# 'COOKRCP01'에서 레시피 목록 가져오기
recipes = data.get("COOKRCP01", {}).get("row", [])

# 데이터프레임 생성
recipe_df = pd.DataFrame(recipes, columns=["RCP_NM", "RCP_PARTS_DTLS"])
recipe_df.index += 1  # 인덱스 1부터 시작

# 메뉴 목록 출력
print(recipe_df[["RCP_NM"]])

# 사용자 입력을 받아 레시피 선택
try:
    n = int(input("\n원하는 레시피 번호를 입력하세요: "))
    if 1 <= n <= len(recipe_df):
        selected_recipe = recipe_df.iloc[n - 1]

        # 선택된 레시피 이름을 파일에 저장
        with open("selected_recipe.txt", "w", encoding="utf-8") as f:
            f.write(selected_recipe["RCP_NM"])

        print(f"\n선택된 레시피: {selected_recipe['RCP_NM']}")
    else:
        print("잘못된 입력입니다. 1부터", len(recipe_df), "사이의 숫자를 입력하세요.")
except ValueError:
    print("잘못된 입력입니다! 숫자를 입력하세요.")