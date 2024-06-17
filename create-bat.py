"creates a bat file to run the python script on windows"
import os
import sys

if __name__ == '__main__':
    with open("fooocus_tg.bat", "w") as f:
        python_interpreter_path = sys.executable
        absolute_path = os.path.abspath("fooocus_tg.py")
        f.write(f"{python_interpreter_path} {absolute_path}\npause")
