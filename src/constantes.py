"""Constantes du jeu UrWorld"""

import time
import pickle
import os
from tkinter import *


def truncature(x, precision=2):
    new_x = str(x)[:precision+2]
    return float(new_x)


t = Tk()
taille_fenetre_largeur_win = t.winfo_screenwidth()
taille_fenetre_hauteur = t.winfo_screenheight()
t.destroy()

# Paramètres de la fenêtre
nombre_sprite_cote = 20
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite

LOGGER_INDENTATION = 2

#variables
structure = []
var_equipement = 3
int_cpt = 0
transparence = 250
monnaie = 5000
fps = 50
x = 0
y = 0
dossier_personnage = "0" + os.sep
arme_personnage = ""
equipement_en_cours = ""
pseudo = ""
mode_de_jeu = False
pas_de_partie = True

valeur_transparence_eau = 156


cds = {
    'qs': None,
    'sd': None,
    'df': None,
    'fg': None
}

with open(".." + os.sep + "assets" + os.sep + "Textes" + os.sep + "passants.pkl", "rb") as passants_lire_txt:
    parole_passants = pickle.Unpickler(passants_lire_txt).load()