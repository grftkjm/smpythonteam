import tkinter as tk
import subprocess  # recipe.py 실행을 위해 사용
from tkinter import messagebox

# 파일 경로
INGREDIENT_FILE = "data/ingredient.txt"

# ingredient.txt 내용 불러오기
def load_ingredient_info():
    try:
        with open(INGREDIENT_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "ingredient.txt 파일을 찾을 수 없습니다."

# "예" 선택 시 recipe.py 실행 후 GUI 종료
def run_recipe():
    root.destroy()
    subprocess.run(["python", "src/recipe.py"])  # recipe.py 실행

# "아니오" 선택 시 메시지 표시 후 GUI 종료
def finish_process():
    messagebox.showinfo("완료", "모든 과정이 완료되었습니다.")
    root.destroy()

# GUI 설정
root = tk.Tk()
root.title("메뉴 정보")
root.geometry("500x500")

# ingredient.txt 내용 표시
ingredient_info = load_ingredient_info()
label = tk.Label(root, text=ingredient_info, font=("Arial", 12), justify="left", wraplength=480)
label.pack(pady=10)

# 레시피 제공 여부 질문
question_label = tk.Label(root, text="레시피를 알려드릴까요?", font=("Arial", 14))
question_label.pack(pady=10)

# 버튼 설정
btn_yes = tk.Button(root, text="예", command=run_recipe, width=10)
btn_yes.pack(pady=5)

btn_no = tk.Button(root, text="아니오", command=finish_process, width=10)
btn_no.pack(pady=5)

root.mainloop()