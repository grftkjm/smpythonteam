import tkinter as tk
import requests
import json
import subprocess  # menu_select.py 실행을 위해 사용
from tkinter import messagebox

# API URL
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

# 파일 경로
MENU_FILE = "data/menu_list.txt"

# 재료 입력 후 검색
def search_recipes():
    ingredient = entry.get().strip()
    
    if not ingredient:
        messagebox.showerror("오류", "재료를 입력하세요.")
        return
    
    response = requests.get(API_URL)
    data = response.json()
    matched_menus = []
    
    for item in data["COOKRCP01"]["row"]:
        menu_name = item["RCP_NM"]
        ingredients = item.get("RCP_PARTS_DTLS", "")
        
        if ingredient in ingredients:  # 입력한 재료가 포함된 메뉴 확인
            matched_menus.append(menu_name)
    
    # 파일 저장
    with open(MENU_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(matched_menus))
    
    messagebox.showinfo("완료", "메뉴 리스트를 저장했습니다.")
    root.destroy()
    subprocess.run(["python", "src/menu_select.py"])  # menu_select.py 실행

# GUI 설정
root = tk.Tk()
root.title("보유 재료 기반 레시피 검색")
root.geometry("400x200")

label = tk.Label(root, text="보유한 재료를 입력하세요:", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

btn_search = tk.Button(root, text="레시피 찾기", command=search_recipes, width=15)
btn_search.pack(pady=10)

root.mainloop()