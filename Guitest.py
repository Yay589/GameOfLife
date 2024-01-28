import subprocess
from parametre import Relancer, graphicalInterfaceON

PYTHON_EXECUTABLE = "C:/Users/Administrator/AppData/Local/Programs/Python/Python311/python.exe"

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
    run_subprocess("d:/python/GameOfLife/configurationpartie.py")
    run_subprocess("d:/python/GameOfLife/paramprimaire.py")
    run_subprocess("d:/python/GameOfLife/paramsecondaire.py")

    if graphicalInterfaceON:
        modify_parametre_file("Relancer", False)
        run_subprocess("d:/python/GameOfLife/maintest.py")
    else:
        run_subprocess("d:/python/GameOfLife/maintesttapha.py")

    while Relancer:
        run_subprocess("d:/python/GameOfLife/configurationpartie.py")
        run_subprocess("d:/python/GameOfLife/paramprimaire.py")
        run_subprocess("d:/python/GameOfLife/paramsecondaire.py")

        if graphicalInterfaceON:
            modify_parametre_file("Relancer", False)
            run_subprocess("d:/python/GameOfLife/maintest.py")
        else:
            run_subprocess("d:/python/GameOfLife/maintesttapha.py")

if __name__ == "__main__":
    start()