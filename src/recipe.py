import os
import requests
from PIL import Image
import io

# API 주소 설정
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/1000"

def get_recipe(menu_name):
    """ API에서 해당 메뉴의 레시피와 이미지 URL 가져옴 """
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()["COOKRCP01"]["row"]
        for menu in data:
            if menu["RCP_NM"] == menu_name:
                recipe_steps = {key: value for key, value in menu.items() if key.startswith("MANUAL")}
                image_url = menu.get("ATT_FILE_NO_MK", "")  # ✅ 이미지 URL 가져오기
                return recipe_steps, image_url
    return None, None

def download_image(image_url, save_path):
    """ 이미지 다운로드 후 저장 """
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        image.save(save_path)
        return save_path
    return None

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "..", "data")
ingredient_file_path = os.path.join(data_dir, "ingredient.txt")
image_file_path = os.path.join(data_dir, "recipe_image.jpg")

# ✅ `ingredient.txt`에서 메뉴명 읽기
if not os.path.exists(ingredient_file_path):
    print("❌ 식재료 정보 파일이 존재하지 않습니다.")
    exit()

with open(ingredient_file_path, "r", encoding="utf-8") as f:
    menu_name = f.readline().strip()  # 첫 번째 줄은 메뉴명

# ✅ API에서 레시피 및 이미지 가져오기
recipe_steps, image_url = get_recipe(menu_name)

if not recipe_steps:
    print(f"\n❌ '{menu_name}'의 레시피를 API에서 찾을 수 없습니다.")
    exit()

# ✅ 레시피 출력 (사용자가 Enter 키를 누르면 다음 단계로 이동)
print(f"\n🍽️ 선택한 메뉴: {menu_name}\n")
print("📜 레시피 단계별 안내:")
for i, step in sorted(recipe_steps.items()):
    if not step.strip():  # ✅ 값이 비어 있으면 즉시 종료
        break
    input(f"\n🔹 {step}\n👉 다음 단계로 진행하려면 Enter 키를 누르세요...")

# ✅ 모든 단계 완료 후 이미지 출력 여부 확인
print("\n🎉 모든 과정이 완료되었습니다! 맛있게 드세요! 🍽️")

if image_url:
    show_image = input("\n📷 요리 이미지를 보여드릴까요? (예/아니오): ").strip().lower()
    if show_image in ["예", "y"]:
        downloaded_image = download_image(image_url, image_file_path)
        if downloaded_image:
            print(f"\n📷 요리 이미지가 저장되었습니다: {downloaded_image}")
            image = Image.open(downloaded_image)
            image.show()  # ✅ 이미지 출력
        else:
            print("\n⚠️ 이미지 다운로드에 실패했습니다.")
    else:
        print("\n❌ 이미지를 표시하지 않습니다.")
else:
    print("\n⚠️ 해당 메뉴의 요리 이미지를 API에서 찾을 수 없습니다.")