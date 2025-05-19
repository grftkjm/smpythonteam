import os
import subprocess

# 프로젝트 폴더 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, "src")

# 실행할 파일 목록
scripts = ["TDEE.py", "option_select.py", "menu_select.py", "ingredient_display.py"]

# 순서대로 실행
for script in scripts:
    script_path = os.path.join(src_dir, script)
    
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"\n❌ 파일을 찾을 수 없습니다: {script_path}. 확인해주세요.")