import os
import glob

def restart():
    try:
        to_delete = glob.glob(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "*.sav")
        for i in to_delete:
            os.remove(i)
        to_delete = glob.glob(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "Olds Maps" + os.sep + "*.lvl")
        for j in to_delete:
            os.remove(j)
        os.remove(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")
    except OSError:
        print("Une erreur est survenue.")
        return False
    else:
        print("Formatage réussi !")
        return True