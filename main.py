import subprocess

def start():
    while True:
        print(" ---------------------------------------")
        print("|   Bienvenue dans le menu principal    |")
        print("| ---------------------------------------")
        print("|      Veuillez choisir une option      |")
        print("|    1-  Interface Graphique            |")
        print("|    2-  Interface Console.             |")
        print("|    3-      Quitter                    |")
        print(" ---------------------------------------")
        
        x = input()
        
        if x == "1":
            print("Chargement de l'interface graphique en cours..")
            subprocess.run(["python3", "Gui.py"])
        elif x == "2":
            print("Chargement de l'interface console en cours..")
            subprocess.run(["python3", "maintesttapha.py"])
        elif x == "3":
            print("Au revoir")
            break
        else:
            print("Veuillez choisir une option entre 1, 2 ou 3")

if __name__ == "__main__":
    start()
