import os
import glob

def restart():
    try:
        to_delete = glob.glob("Parties" + os.sep + "*.sav")
        for i in to_delete:
            os.remove(i)
        to_delete = glob.glob("Niveaux" + os.sep + "Olds Maps" + os.sep + "*.lvl")
        for j in to_delete:
            os.remove(j)
        os.remove("Niveaux" + os.sep + "map.lvl")
    except OSError:
        print("Une erreur est survenue, veuillez relancer le jeu (main.py), le fermer, puis réessayer.")
        return False
    else:
        print("Formatage réussi !")
        return True