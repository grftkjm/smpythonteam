import tkinter as tk
import requests
import json
import subprocess 
import os  
from tkinter import messagebox

# 파일 경로
INGREDIENT_FILE = "data/ingredient.txt"
IMAGE_FILE = "data/recipe_image.jpg"

# API URL
API_URL = "http://openapi.foodsafetykorea.go.kr/api/7904b29570d44de38aa6/COOKRCP01/json/1/500"

# 메뉴명 가져오기 (ingredient.txt에서 메뉴명만 가져옴)
def get_menu_name():
    try:
        with open(INGREDIENT_FILE, "r", encoding="utf-8") as file:
            return file.readline().strip().replace("메뉴명: ", "")  
    except FileNotFoundError:
        return None

# 메뉴 레시피 가져오기
def fetch_recipe(menu_name):
    response = requests.get(API_URL)
    data = response.json()

    for item in data["COOKRCP01"]["row"]:
        if item["RCP_NM"] == menu_name:
            recipe_steps = []
            for i in range(1, 21): 
                step_key = f"MANUAL{str(i).zfill(2)}" 
                step = item.get(step_key, "").strip()
                if not step: 
                    break
                recipe_steps.append(step)

            image_url = item.get("ATT_FILE_NO_MAIN", None)

            return recipe_steps, image_url

    return None, None

# GUI 설정
root = tk.Tk()
root.title("레시피 진행")
root.geometry("500x300")

menu_name = get_menu_name()
if not menu_name:
    messagebox.showerror("오류", "ingredient.txt에서 메뉴명을 찾을 수 없습니다.")
    root.quit()  # 프로그램 정상 종료

recipe_steps, image_url = fetch_recipe(menu_name)
if not recipe_steps:
    messagebox.showerror("오류", "해당 메뉴의 레시피를 찾을 수 없습니다.")
    root.quit()  # 프로그램 정상 종료

# 레시피 진행 변수
current_step = 0

# 레시피 진행 함수
def next_step():
    global current_step
    if current_step < len(recipe_steps):
        label_recipe.config(text=recipe_steps[current_step])
        current_step += 1
    else:
        ask_image()  # 레시피 종료 후 이미지 출력 여부 질문

# 이미지 출력 여부 질문
def ask_image():
    result = messagebox.askyesno("레시피 완료", "완성! 이미지를 출력할까요?")
    if result:
        download_and_show_image()
    else:
        finish_process()

# 이미지 다운로드 및 실행
def download_and_show_image():
    if image_url:
        response = requests.get(image_url)
        with open(IMAGE_FILE, "wb") as file:
            file.write(response.content)
        
        messagebox.showinfo("이미지 저장 완료", "레시피 이미지가 저장되었습니다.")
        subprocess.run(["start", IMAGE_FILE], shell=True)  # 이미지 실행
    finish_process()

# 모든 과정 완료 메시지
def finish_process():
    messagebox.showinfo("완료", "모든 과정이 종료되었습니다.")
    root.destroy()

# 레시피 표시
label_title = tk.Label(root, text=f"{menu_name} 레시피", font=("Arial", 16))
label_title.pack(pady=10)

label_recipe = tk.Label(root, text="", font=("Arial", 12), wraplength=480)
label_recipe.pack(pady=10)

btn_next = tk.Button(root, text="다음", command=next_step, width=10)
btn_next.pack(pady=10)

next_step() 

root.mainloop()