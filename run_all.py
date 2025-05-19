import subprocess
import os

# 실행할 파일 목록 (순서 변경: TDEE 먼저 실행)
files_to_run = ["TDEE.py", "menu_selection.py", "menu_save.py", "ingredient_display.py"]

for file in files_to_run:
    if not os.path.exists(file):
        exit()

    subprocess.run(["python", file])