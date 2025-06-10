import tkinter as tk
import requests
import json
import subprocess 
from tkinter import ttk, messagebox

# API URL
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

# 운동량 리스트
ACTIVITY_LEVELS = {
    "거의 운동하지 않음": 1.2,
    "간단한 운동(주 1~3회)": 1.375,
    "규칙적 운동(주 3~5회)": 1.55,
    "활발한 운동(주 6~7회)": 1.725,
    "운동선수 수준 운동": 1.9,
}

# TDEE 계산 함수
def calculate_tdee(weight, height, age, gender, activity_level):
    if gender == "남성":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    return bmr * ACTIVITY_LEVELS[activity_level]

# 목표 감량 적용
def adjust_calories(tdee, weight_loss_goal):
    if weight_loss_goal > 1.5:
        messagebox.showwarning("경고", "건강을 위해 목표 감량을 최대 1.5kg로 제한합니다.")
        weight_loss_goal = 1.5  # 자동 제한

    daily_calories = tdee - (7700 * weight_loss_goal / 7)  # 7700kcal = 1kg 감량
    return daily_calories

# 메뉴 데이터 가져오기 (INFO_ENG 사용)
def fetch_menu(menu_type, daily_kcal=None):
    response = requests.get(API_URL)
    data = response.json()
    menus = []

    kcal_limit = None
    if menu_type == "다이어트식":
        kcal_limit = daily_kcal / 3
    elif menu_type == "밥과 함께":
        kcal_limit = (daily_kcal / 3) - 300

    for item in data["COOKRCP01"]["row"]:
        menu_name = item["RCP_NM"]
        try:
            menu_kcal = float(item["INFO_ENG"])  # INFO_ENG 값 가져오기
        except ValueError:
            menu_kcal = 99999  # 칼로리 정보 없는 경우 제외

        if menu_type == "일반식" or (kcal_limit and menu_kcal <= kcal_limit):
            menus.append(f"{menu_name} - {menu_kcal} kcal")  # 메뉴명과 열량 저장

    # 조건을 만족하는 메뉴가 없으면 일반식 추천
    if not menus and menu_type != "일반식":
        messagebox.showinfo("알림", "사용자에게 맞는 메뉴를 찾을 수 없습니다. 일반식 메뉴를 추천해드릴게요.")
        return fetch_menu("일반식")

    # 파일 저장
    with open("data/menu_list.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(menus))

    result_label.config(text=f"{menu_type} 레시피 {len(menus)}개 저장 완료!")

    # 모든 작업 완료 후 GUI 종료 및 menu_select.py 실행
    root.after(2000, lambda: close_and_run_next())

# GUI 종료 후 menu_select.py 실행 함수
def close_and_run_next():
    root.destroy()
    subprocess.run(["python", "src/menu_select.py"])  # menu_select.py 실행

# TDEE 입력 창
def open_tdee_window(menu_type):
    tdee_window = tk.Toplevel(root)
    tdee_window.title("TDEE 계산")

    labels = ["키(cm)", "몸무게(kg)", "나이", "성별(남성/여성)"]
    entries = {label: tk.Entry(tdee_window) for label in labels}

    for label, entry in entries.items():
        tk.Label(tdee_window, text=label).pack()
        entry.pack()

    tk.Label(tdee_window, text="운동량 선택").pack()
    activity_var = tk.StringVar()
    activity_combobox = ttk.Combobox(tdee_window, textvariable=activity_var, values=list(ACTIVITY_LEVELS.keys()), state="readonly")
    activity_combobox.pack()
    activity_combobox.current(0)

    def calculate():
        height = float(entries["키(cm)"].get())
        weight = float(entries["몸무게(kg)"].get())
        age = int(entries["나이"].get())
        gender = entries["성별(남성/여성)"].get()
        activity_level = activity_var.get()

        tdee = calculate_tdee(weight, height, age, gender, activity_level)
        goal_loss = float(entries["일주일 목표 감량(kg)"].get())

        daily_kcal = adjust_calories(tdee, goal_loss)

        messagebox.showinfo("TDEE 결과", f"당신의 하루 권장 섭취 칼로리: {int(daily_kcal)} kcal")

        tdee_window.after(2000, tdee_window.destroy)  # 2초 후 창 닫기
        fetch_menu(menu_type, daily_kcal)  # TDEE 적용된 메뉴 가져오기

    tk.Label(tdee_window, text="일주일 목표 감량(kg)").pack()
    entries["일주일 목표 감량(kg)"] = tk.Entry(tdee_window)
    entries["일주일 목표 감량(kg)"].pack()
    
    tk.Button(tdee_window, text="TDEE 계산 및 메뉴 가져오기", command=calculate).pack()

# GUI 설정
root = tk.Tk()
root.title("다이어트 레시피 선택")
root.geometry("400x400")

label = tk.Label(root, text="식단을 선택하세요!", font=("Arial", 14))
label.pack(pady=10)

# 메뉴 선택 버튼
btn_normal = tk.Button(root, text="🍽 일반식", width=30, command=lambda: fetch_menu("일반식"))
btn_normal.pack(pady=5)

btn_diet = tk.Button(root, text="🥗 다이어트식", width=30, command=lambda: open_tdee_window("다이어트식"))
btn_diet.pack(pady=5)

btn_mixed_diet = tk.Button(root, text="🍛 밥과 함께 먹을 다이어트식", width=30, command=lambda: open_tdee_window("밥과 함께"))
btn_mixed_diet.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()