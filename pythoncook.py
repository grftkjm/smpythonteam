import os
import subprocess

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")

# 실행할 파일 목록
scripts = ["option_select.py", "menu_select.py", "ingredient_display.py"]

# 각 단계 실행
for script in scripts:
    script_path = os.path.join(src_dir, script)
    subprocess.run(["python", script_path])