import os
import glob
import pickle

print("Attention ! Vous allez entrer dans une zone de non retour !")
print("Si ne savez ce que faites, fermez cette fenetre.\n\n")

print("Entrez le nom du fichier que vous voulez récupérer : ")
fname = input("../assets/Save/")
while fname not in glob.glob(".." + os.sep + "assets" + os.sep  "Save" + os.sep + "*.sav"):
    print("Entrez le nom du fichier que vous voulez récupérer : ")
    fname = input("../assets/Save/")

if input("Voulez vous récupérer les données ou tout réécrire ? ").lower() == 'o':
    with open(".." + os.sep + "assets" + os.sep  "Save" + os.sep + fname, "rb") as readb:
        with open("recovered.txt", "w") as writef:
            writef.write(pickle.Unpickler(readb).load())
else:
    print("Veuillez écrire votre code pour " + fname + " dans recovery.txt")

input("Appuyez sur entrée quand vos modifications seront terminées dans recovered.txt ...")
print("\nTéléversement du contenu de recovered.txt dans " + fname + " ...")

if input("Etes vous sur de vouloir continuer [o|n] ? ").lower() == 'o':
    with open(".." + os.sep + "assets" + os.sep  "Save" + os.sep + fname, "wb") as writeb:
        with open("recovered.txt", "r") as readf:
            pickle.Pickler(writeb).dump(eval(readf))
    input("Téléversement terminé.")