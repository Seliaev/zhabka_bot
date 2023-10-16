import sys
import os


def restart_script():
    python_executable = sys.executable
    root = os.getcwd()
    script_file = "main.py"
    file_path = os.path.join(root, script_file)
    os.execv(python_executable, ['python', file_path])

