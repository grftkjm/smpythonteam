import tkinter as tk
import subprocess   
import os  

# 파일 초기화 함수
def clear_data_folder():
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

    # 파일 삭제 (txt, jpg)
    for file in os.listdir(data_folder):
        if file.endswith(".txt") or file.endswith(".jpg"):
            os.remove(os.path.join(data_folder, file))

# 초기화 실행
clear_data_folder()

# GUI 설정
root = tk.Tk()
root.title("PythonCook")
root.geometry("350x250")

# 실행 함수
def run_script(script_name):
    subprocess.run(["python", f"src/{script_name}"])
    root.destroy()  # 선택 후 프로그램 자동 종료

# 라벨 추가
label = tk.Label(root, text="레시피를 선택하세요!", font=("Arial", 14))
label.pack(pady=10)

# 버튼 추가
btn_diet = tk.Button(root, text="다이어트를 위한 레시피", width=25, command=lambda: run_script("diet_option.py"))
btn_diet.pack(pady=5)

btn_ingredient = tk.Button(root, text="보유 재료 기반 레시피", width=25, command=lambda: run_script("ingredient_select.py"))
btn_ingredient.pack(pady=5)

btn_type = tk.Button(root, text="음식 유형별 레시피", width=25, command=lambda: run_script("type_select.py"))
btn_type.pack(pady=5)

# GUI 실행
root.mainloop()