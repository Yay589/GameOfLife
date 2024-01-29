import subprocess
import time
from parametre import Relancer, graphicalInterfaceON

PYTHON_EXECUTABLE = "python3"

def modify_parametre_file(key_to_modify, new_value):
    with open("parametre.py", 'r') as file:
        lines = file.readlines()

    with open("parametre.py", 'w') as file:
        for line in lines:
            if line.startswith(key_to_modify):
                line = f"{key_to_modify} = {new_value}\n"
            file.write(line)

def run_subprocess(script_path):
    subprocess.run([PYTHON_EXECUTABLE, script_path])

def start():
    run_subprocess("configurationpartie.py")
    time.sleep(0.1)
    run_subprocess("paramprimaire.py")
    time.sleep(0.1)
    run_subprocess("paramsecondaire.py")
    time.sleep(0.1)

    if graphicalInterfaceON:
        modify_parametre_file("Relancer", False)
        run_subprocess("maintest.py")
        time.sleep(0.1)
    else:
        run_subprocess("maintesttapha.py")
        time.sleep(0.1)

    while Relancer:
        run_subprocess("configurationpartie.py")
        time.sleep(0.1)
        run_subprocess("paramprimaire.py")
        time.sleep(0.1)
        run_subprocess("paramsecondaire.py")
        time.sleep(0.1)

        if graphicalInterfaceON:
            modify_parametre_file("Relancer", False)
            run_subprocess("maintest.py")
            time.sleep(0.1)
        else:
            run_subprocess("maintesttapha.py")
            time.sleep(0.1)

if __name__ == "__main__":
    start()