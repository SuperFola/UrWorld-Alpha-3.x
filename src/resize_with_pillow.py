from PIL import Image as PILImage
import glob
import os

miniaturisation = True

def img_resize(filename, taille):
    """
    fonction pour changer la taille d'une image et l'enregistrer
    filename : nom du l'image a changer de taille
    taille : nouvelle taille
    """
    file, ext = os.path.splitext(filename)
    im = PILImage.open(filename)
    w, h = im.size
    im.thumbnail((taille, int(taille*h/w)), PILImage.ANTIALIAS)
    im.save(str(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "thumbnail" + os.sep + os.path.split(file)[1] + "_thumbnail" + ext), 'PNG')

#miniatures
def start():
    if miniaturisation is True:
        print('Creation des miniatures ...')
        for fichier in glob.glob(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "*.png"):
            img_resize(fichier, 10)
        img_resize(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + "C" + os.sep + "perso.png", 10)
        for fichier in glob.glob(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "Electricity" + os.sep + "*.png"):
            img_resize(fichier, 10)