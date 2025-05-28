import tkinter as tk
import requests
import json
import subprocess  # 추가: ingredient_display.py 실행을 위해 사용
from tkinter import ttk, messagebox

# API URL
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

# 파일 경로
MENU_FILE = "data/menu_list.txt"
INGREDIENT_FILE = "data/ingredient.txt"

# 메뉴 리스트 가져오기 (열량 포함하여 표시)
def load_menu_list():
    try:
        with open(MENU_FILE, "r", encoding="utf-8") as file:
            return file.read().splitlines()  # 그대로 불러옴 (메뉴명 + 열량)
    except FileNotFoundError:
        return []

# 메뉴 정보 가져오기 (API에서 메뉴명만 대조)
def fetch_menu_details(selected_menu):
    menu_name = selected_menu.split(" - ")[0]  # 열량 제거하고 메뉴명만 사용

    response = requests.get(API_URL)
    data = response.json()
    
    for item in data["COOKRCP01"]["row"]:
        if item["RCP_NM"] == menu_name:  # 오직 메뉴명만 비교
            ingredients = item.get("RCP_PARTS_DTLS", "정보 없음")
            nutrition = f"나트륨: {item.get('INFO_NA', '정보 없음')} mg\n"
            nutrition += f"탄수화물: {item.get('INFO_CAR', '정보 없음')} g\n"
            nutrition += f"단백질: {item.get('INFO_PRO', '정보 없음')} g\n"
            nutrition += f"지방: {item.get('INFO_FAT', '정보 없음')} g\n"
            nutrition += f"열량: {item.get('INFO_ENG', '정보 없음')} kcal\n"

            # 파일 저장
            with open(INGREDIENT_FILE, "w", encoding="utf-8") as file:
                file.write(f"메뉴명: {menu_name}\n\n[식재료]\n{ingredients}\n\n[영양 정보]\n{nutrition}")

            # 메시지 표시 후 GUI 종료 및 ingredient_display.py 실행
            messagebox.showinfo("저장 완료", "메뉴 정보를 저장했습니다.")
            root.after(500, close_and_run_next)  # 0.5초 후 종료 및 실행
            return
    
    messagebox.showerror("오류", "해당 메뉴 정보를 찾을 수 없습니다.")

# GUI 종료 후 ingredient_display.py 실행 함수
def close_and_run_next():
    root.destroy()
    subprocess.run(["python", "src/ingredient_display.py"])  # ingredient_display.py 실행

# GUI 설정
root = tk.Tk()
root.title("메뉴 선택")
root.geometry("400x400")

label = tk.Label(root, text="메뉴를 선택하세요!", font=("Arial", 14))
label.pack(pady=10)

menu_list = load_menu_list()

# 메뉴 선택 리스트 (열량 포함된 형태로 표시)
menu_var = tk.StringVar()
menu_dropdown = tk.OptionMenu(root, menu_var, *menu_list)
menu_dropdown.pack(pady=10)

# 선택 버튼
btn_select = tk.Button(root, text="메뉴 선택", command=lambda: fetch_menu_details(menu_var.get()))
btn_select.pack(pady=10)

root.mainloop()