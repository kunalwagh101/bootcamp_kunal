from pathlib import Path
import subprocess
import re

def natural_sort_key(path: Path):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', path.name)]


current_folder = Path.cwd()
py_files = list(current_folder.glob("ex_*.py"))
py_files.sort(key=natural_sort_key)

for py_file in py_files:
    print(f"\n=== Running {py_file.name} ===\n")
    
    try:
        subprocess.run(["python", str(py_file)], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f" Error: {py_file.name} failed with exit code {e.returncode}. Skipping...")
    except Exception as e:
        print(f" Unexpected error while running {py_file.name}: {e}. Skipping...")

print("\n Execution completed.")
