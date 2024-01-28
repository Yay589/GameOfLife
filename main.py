import subprocess

def start():
    while True:
        print(" _______________________________________")
        print("|                                       |")
        print("|   Bienvenue dans le menu principal    |")
        print("|_______________________________________|")
        print("|                                       |")
        print("|      Veuillez choisir une option      |")
        print("|    1-  Interface Graphique            |")
        print("|    2-  Interface Console.             |")
        print("|    3-      Quitter                    |")
        print("|_______________________________________|")
        
        x = input()
        
        if x == "1":
            print("Chargement de l'interface graphique en cours..")
            
            subprocess.run(["C:/Users/Administrator/AppData/Local/Programs/Python/Python311/python.exe", "d:/python/GameOfLife/maintest.py"])
        elif x == "2":
            print("Chargement de l'interface console en cours..")
            subprocess.run(["C:/Users/Administrator/AppData/Local/Programs/Python/Python311/python.exe", "maintesttapha.py"])
        elif x == "3":
            print("Au revoir")
            break
        else:
            print("Veuillez choisir une option entre 1, 2 ou 3")

if __name__ == "__main__":
    start()
