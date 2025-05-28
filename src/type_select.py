import tkinter as tk
import requests
import json
import subprocess  # menu_select.py 실행을 위해 사용
from tkinter import messagebox

# API URL
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

# 파일 경로
MENU_FILE = "data/menu_list.txt"

# 음식 유형 검색 함수
def search_recipes(food_type):
    response = requests.get(API_URL)
    data = response.json()
    matched_menus = []

    for item in data["COOKRCP01"]["row"]:
        if item.get("RCP_PAT2") == food_type:
            matched_menus.append(item["RCP_NM"])

    # 메뉴 리스트 저장
    with open(MENU_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(matched_menus))

    messagebox.showinfo("완료", "메뉴 리스트를 저장했습니다.")
    root.destroy()
    subprocess.run(["python", "src/menu_select.py"])  # menu_select.py 실행

# GUI 설정
root = tk.Tk()
root.title("음식 유형 선택")
root.geometry("400x300")

label = tk.Label(root, text="원하는 음식 유형을 선택하세요!", font=("Arial", 14))
label.pack(pady=10)

# 버튼 추가
btn_soup = tk.Button(root, text="🍲 국 & 찌개", width=20, command=lambda: search_recipes("국&찌개"))
btn_soup.pack(pady=5)

btn_side = tk.Button(root, text="🥗 반찬", width=20, command=lambda: search_recipes("반찬"))
btn_side.pack(pady=5)

btn_main = tk.Button(root, text="🍛 일품", width=20, command=lambda: search_recipes("일품"))
btn_main.pack(pady=5)

btn_dessert = tk.Button(root, text="🍰 후식", width=20, command=lambda: search_recipes("후식"))
btn_dessert.pack(pady=5)

root.mainloop()