# -*-coding: utf8-*

import os
import time
import glob
import ctypes
import pygame
import niveau as niveau_pkg
import personnage_code
import random
import pickle
import tarfile
import socket
import BModules.tree
import tkinter.messagebox
import tkinter.filedialog
from tkinter import *
from tkinter.colorchooser import *
from random import *
from niveau import *
from math import *
from pygame.locals import *
import constantes as cst
from commerces_p import *
from threading import Thread
from BModules.reader import Reader
from BModules.progress_bar import *
from BModules.discussion import *
import items as itm
from Mods import *
import dialog_box as dlb
import weather

taille_fenetre_largeur_win = cst.taille_fenetre_largeur_win

testeur = os.path.exists("test.test")


def jeu(fenetre, choix, dossier_personnage, peacefull, fps, volume_son_j, creatif,
                    root, rcenter, r, nb_blocs_large, en_reseau, hote, port, realistic):
    with open("Parties" + os.sep + "dossier.sav", "wb") as dossier_ecrire:
        pickle.Pickler(dossier_ecrire).dump(dossier_personnage)

    # tres important :
    var_gravite = 0.142  # doit etre supérieur à 20~21_blocs / 150 = MAX >= 0.1401

    boumList = []
    lst_inventaire = ""
    with open("s.sav", "rb") as invent_dd:
        depickle_idd = pickle.Unpickler(invent_dd)
        lst_inventaire = depickle_idd.load()

    action = 'teleporte'

    #les blocks
    blocs = niveau_pkg.Blocks()
    blocs.add('p', solid=True, shadow=0, gravity=False, quantity=0, innafichable=True, name='Bloc indestructible', tps_explode=0, take_fire=False)
    blocs.add('1', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('2', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('3', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('4', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('5', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('6', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('7', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('8', solid=True, shadow=0, gravity=True, quantity=0, innafichable=True, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('Q', solid=False, shadow=0, gravity=False, quantity=10, innafichable=True, name='Potion de Vie', tps_explode=0, take_fire=False)
    blocs.add('S', solid=False, shadow=0, gravity=False, quantity=10, innafichable=True, name='Potion de Mana', tps_explode=0, take_fire=False)
    blocs.add('D', solid=False, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre des Lasers', tps_explode=0, take_fire=False)
    blocs.add('F', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre de Téléportation', tps_explode=0, take_fire=False)
    blocs.add('G', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre de Feu', tps_explode=0, take_fire=False)
    blocs.add('H', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre du Cône', tps_explode=0, take_fire=False)
    blocs.add('J', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre de la Sphère', tps_explode=0, take_fire=False)
    blocs.add('K', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Sceptre de Construction', tps_explode=0, take_fire=False)
    blocs.add('qs', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='CD Jaune', tps_explode=0, take_fire=False)
    blocs.add('sd', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='CD Rose', tps_explode=0, take_fire=False)
    blocs.add('df', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='CD Vert', tps_explode=0, take_fire=False)
    blocs.add('fg', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='CD Violet', tps_explode=0, take_fire=False)
    blocs.add('/§', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Monnaie', tps_explode=0, take_fire=False)
    blocs.add('§%', solid=True, shadow=0, gravity=False, quantity=10, innafichable=True, name='Marteau', tps_explode=0, take_fire=False)
    blocs.add('a', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Minerai d\'Or', tps_explode=0, take_fire=False)
    blocs.add('m', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Planches', tps_explode=0, take_fire=True)
    blocs.add('t', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Tuiles', tps_explode=0, take_fire=False)
    blocs.add('c', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='PNJ', tps_explode=0, take_fire=False)
    blocs.add('r', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Minerai de Charbon', tps_explode=0, take_fire=False)
    blocs.add('u', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Minerai d\'Emeraude', tps_explode=0, take_fire=False)
    blocs.add('y', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Minerai de Diamant', tps_explode=0, take_fire=False)
    blocs.add('i', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Minerai de Rubis', tps_explode=0, take_fire=False)
    blocs.add('M', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Demi bloc de Pierre', tps_explode=0, take_fire=False)
    blocs.add('x', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Briques', tps_explode=0, take_fire=False)
    blocs.add('b', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Planches Sombres', tps_explode=0, take_fire=True)
    blocs.add('n', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Planches Claires', tps_explode=0, take_fire=True)
    blocs.add('?', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Demi bloc de Planches', tps_explode=0, take_fire=True)
    blocs.add('.', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Demi bloc de Planches Sombres', tps_explode=0, take_fire=True)
    blocs.add('/', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Demi bloc de Planches Claires', tps_explode=0, take_fire=True)
    blocs.add('A', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Bleue', tps_explode=0, take_fire=True)
    blocs.add('Z', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Grise', tps_explode=0, take_fire=True)
    blocs.add('E', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Jaune', tps_explode=0, take_fire=True)
    blocs.add('R', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Rouge', tps_explode=0, take_fire=True)
    blocs.add('T', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Verte', tps_explode=0, take_fire=False)
    blocs.add('Y', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Laine Violette', tps_explode=0, take_fire=True)
    blocs.add('U', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Terre', tps_explode=0, take_fire=False)
    blocs.add('I', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Neige', tps_explode=0, take_fire=True)
    blocs.add('s', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Pierre', tps_explode=0, take_fire=False)
    blocs.add('h', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Herbe', tps_explode=0, take_fire=True)
    blocs.add('B', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Jukebox', tps_explode=0, take_fire=True)
    blocs.add('er', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Charbon pur', tps_explode=0, take_fire=True)
    blocs.add('rt', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Diamant pur', tps_explode=0, take_fire=False)
    blocs.add('ty', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Emeraude pure', tps_explode=0, take_fire=False)
    blocs.add('yu', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Or pur', tps_explode=0, take_fire=False)
    blocs.add('ui', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Rubis pur', tps_explode=0, take_fire=False)
    blocs.add('cv', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Bombe Atomique', tps_explode=0, take_fire=False)
    blocs.add('vb', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Téléporteur', tps_explode=0, take_fire=False)
    blocs.add('bn', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Pierre de l\'Eau', tps_explode=0, take_fire=False)
    blocs.add('n?', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Pierre du Feu', tps_explode=0, take_fire=False)
    blocs.add('?.', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Pierre de la Terre', tps_explode=0, take_fire=False)
    blocs.add('d', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Sable', tps_explode=0, take_fire=False)
    blocs.add('%b', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Transpondeur Temporel', tps_explode=0, take_fire=False)
    blocs.add('gh', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Bleue', tps_explode=0, take_fire=False)
    blocs.add('hj', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Grise', tps_explode=0, take_fire=False)
    blocs.add('jk', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Jaune', tps_explode=0, take_fire=False)
    blocs.add('kl', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Marron', tps_explode=0, take_fire=False)
    blocs.add('lm', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Marron Claire', tps_explode=0, take_fire=False)
    blocs.add('mw', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Marron Foncée', tps_explode=0, take_fire=False)
    blocs.add('wx', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Rouge', tps_explode=0, take_fire=False)
    blocs.add('xc', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Table Verte', tps_explode=0, take_fire=False)
    blocs.add('q', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Bibliothèque', tps_explode=0, take_fire=False)
    blocs.add('0', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Vide', tps_explode=0, take_fire=False)
    blocs.add('v', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Verre', tps_explode=0, take_fire=False)
    blocs.add('l', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Verre Bleu', tps_explode=0, take_fire=False)
    blocs.add('k', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Verre Jaune', tps_explode=0, take_fire=False)
    blocs.add('g', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Verre Vert', tps_explode=0, take_fire=False)
    blocs.add('P', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Feuillage', tps_explode=0, take_fire=True)
    blocs.add('f', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Verre Rouge', tps_explode=0, take_fire=False)
    blocs.add('W', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Torche Bleue', tps_explode=0, take_fire=True)
    blocs.add('X', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Torche Verte', tps_explode=0, take_fire=True)
    blocs.add('C', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Torche Jaune', tps_explode=0, take_fire=True)
    blocs.add('V', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Torche Rouge', tps_explode=0, take_fire=True)
    blocs.add('az', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Champignons Blancs', tps_explode=0, take_fire=False)
    blocs.add('ze', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Champignons Rouges', tps_explode=0, take_fire=False)
    blocs.add('io', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Fleur Bleue', tps_explode=0, take_fire=True)
    blocs.add('op', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Fleur Rouge', tps_explode=0, take_fire=True)
    blocs.add('pq', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Fleur Jaune', tps_explode=0, take_fire=True)
    blocs.add('O', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Tronc d\'Arbre', tps_explode=0, take_fire=True)
    blocs.add('./', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Echelle', tps_explode=0, take_fire=True)
    blocs.add('e', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Eau', tps_explode=0, take_fire=False)
    blocs.add('%a', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Pancarte', tps_explode=0, take_fire=True)
    blocs.add('feu', solid=False, shadow=0, gravity=False, quantity=0, innafichable=True, name='Feu', tps_explode=0, take_fire=True)

    liste_septre = [
        'D', 'F',
        'G', 'H',
        'J', 'K'
    ]
    #liste des blocs :
    dico_cd = cst.cds
    liste_pos_a_appliquer = []
    liste_couleur = [
        (23, 220, 189),
        (16, 209, 182),
        (9, 198, 175),
        (2, 187, 168),
        (235, 176, 161),
        (228, 165, 154),
        (221, 154, 147),
        (214, 143, 140),
        (207, 132, 133),
        (200, 121, 126),
        (193, 110, 119)
    ]
    liste_teleporteurs = []
    les_autres = ""
    xy_s, xy_s1, xi, yi = 0, 0, 0, 0
    debut, fin = 0, 204
    x_blit, y_blit = 0, 0
    x_souris, y_souris = 0, 0
    continuer = 1
    nombre_degats = 0
    x, y = 0, 0
    couleur_idd = (80, 65, 85)
    clique_gauche = 0
    cpt_blit_eau = 0
    number_of_case = 0
    last_music_time = 0
    last_vie = 100
    time_flash = 10
    index_couleur = 0
    last_cd_used = ""
    pseudo = ""
    obj_courant = "m"
    numero_niv = "map"
    arme_personnage = ""
    situation_actuelle = ""
    nom_mechant = "Gordavus"
    grd_msg_bjr = "Bonjour toi !"
    last_pos = (0, 0)
    breakListe = []
    windowed_is = False
    show_stats = True
    courir_bool = False
    vip_bool = False
    vu_vip_change = False
    ombrage = True
    prise_de_degats = 0
    annee = 0
    longueur = 90
    saut = False
    last_perso_saut = (0, 0)
    time_saut = 0
    temps_saut_attendre = 0.125
    pancartes_lst = []
    show_cursor = True
    y_ecart = (root.get_size()[1] - 600) // 2
    txt_chat = ""
    time_blitting_txt_chat = 0
    hauteur_saut = 0
    liste_hauteur_saut = [
        -1,
        -1,
        -1,
        +1,
        +1,
        +1,
        +1,
    ]
    nb_cases_chut = 0
    affiche_oth = True
    jump_height = 3

    #VARIABLES INDISPENSABLES AU SCROLLING HORIZONTAL:
    max_scrolling = 20 * fin  #maximum du scrolling

    with open("Parties" + os.sep + "pseudo.sav", "r") as nom_perso:  #pour le pseudo
        pseudo = nom_perso.read()
        with open("bonjour.txt", "r") as msg_bjr_lire:
            grd_msg_bjr = str(msg_bjr_lire.read()).format(pseudo, nom_mechant)
            grd_msg_bjr += "\n" * 4 + "Bonne aventure `{0}` !".format(pseudo)
    with open("Personnage" + os.sep + "A" + os.sep + "arme.txt", "r") as lire_nom_arme:
        arme_personnage = lire_nom_arme.read()
    if os.path.exists("Personnage" + os.sep + "0" + os.sep + "vip.file"):
        with open("Personnage" + os.sep + "0" + os.sep + "vip.file", "r") as lire_vip:
            if lire_vip.read() == pseudo + "::VIP":
                vip_bool = True
            else:
                vip_bool = False

    #sons
    music_liste = [
        "Sons" + os.sep + "urworld1.wav",
        "Sons" + os.sep + "urworld2.wav"
                   ]
    volume = pygame.mixer.music.get_volume()  #Retourne la valeur du volume, entre 0 et 1
    pygame.mixer.music.set_volume(volume_son_j / 4 * 3)  #Réglage du volume
    eau_bruit = pygame.mixer.Sound("Sons" + os.sep + "water.wav")
    falling = pygame.mixer.Sound("Sons" + os.sep + "falling.wav")
    explode = pygame.mixer.Sound("Sons" + os.sep + "explode.wav")
    breaking_bloc = pygame.mixer.Sound("Sons" + os.sep + "wooden.wav")

    #images
    #police
    font = pygame.font.Font("freesansbold.otf", 8)
    grd_font = pygame.font.Font("freesansbold.otf", 12)
    #pseudo
    pseudo_aff = font.render(pseudo, 1, (10, 10, 10))
    #canne a peche, selecteur, inventaire rapide et monstre (les noms parlent d'eux meme)
    monstre = pygame.image.load("Personnage" + os.sep + "M" + os.sep + "monstre.png").convert_alpha()
    selection_bloc = pygame.image.load("Fond" + os.sep + "selec.png").convert_alpha()
    #les equipements vers la gauche !
    arme_h_g = pygame.image.load("Personnage" + os.sep + "A" + os.sep + "sword_up_g.png").convert_alpha()
    #personnage(s)
    monstres_ou_pas = [6, 7, 8, 9]  #niveaux où les monstres apparaissent
    #items
    marteau = itm.Marteau(rcenter, fenetre, font)
    #reseau
    params_co = ('', 0)

    #variables
    if not en_reseau:
        carte = Carte(fenetre, root, marteau, nb_blocs_large, blocs)
        carte.load("Niveaux" + os.sep + "map.lvl")
    else:
        try:
            socket_client_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            params_co = (hote, port)
            socket_client_serv.sendto(pickle.dumps([pseudo, 0, 0, dossier_personnage]), params_co)
            carte = LANMap(fenetre, root, marteau, nb_blocs_large, socket_client_serv, params_co, blocs)
            carte.receive_map()
        except OSError:
            en_reseau = False
            message_affiche("Le serveur n'est pas joignable, le jeu quitte le mode réseau.", rcenter)
            carte = Carte(fenetre, root, marteau, nb_blocs_large, blocs)
            carte.load("Niveaux" + os.sep + "map.lvl")

    #personnage in game
    if not en_reseau:
        personnage = personnage_code.Personnage(fenetre, dossier_personnage, carte, rcenter, blocs)
    else:
        personnage = personnage_code.Personnage(fenetre, dossier_personnage, carte,
                                                rcenter, blocs, socket_serv=socket_client_serv,
                                                addr=params_co, lan=True)
    #on créé la météo
    vent = weather.Wind(carte, fenetre, personnage)
    pluie = weather.Rain(carte, fenetre, personnage, blocs)
    orage = weather.Storm(carte, fenetre, personnage)
    #on ajoute la météo à la carte
    carte.set_meteo('')


    def sauvegarder(quitte, perso, equipement_courant,
                    ombrage, teleporteurs, creatif, pancartes_lst, carte):
        #def de sauvegarde
        print("\n\n" + "*" * 34 + " SAUVEGARDE " + "*" * 34 + "\n")
        #avec Pickle
        with open("Parties" + os.sep + "equipement_en_cours.sav", "wb") as ecrire_equipement:
            pickle.Pickler(ecrire_equipement).dump(equipement_courant)
        with open("Parties" + os.sep + "niveau.sav", "wb") as niv_ecrire:
            pickle.Pickler(niv_ecrire).dump(numero_niv)
        with open("Parties" + os.sep + "bloc.sav", "wb") as bloc_save:
            pickle.Pickler(bloc_save).dump(blocs)
        with open("Parties" + os.sep + "pos.sav", "wb") as pos_save:
            pickle.Pickler(pos_save).dump(personnage.get_pos())
        with open("Parties" + os.sep + "fov.sav", "wb") as fov_ecrire:
            pickle.Pickler(fov_ecrire).dump(carte.get_fov())
        with open("Parties" + os.sep + "mana.sav", "wb") as mana_ecrire:
            pickle.Pickler(mana_ecrire).dump(perso.get_mana())
        with open("Parties" + os.sep + "couleur.sav", "w") as couleur_ecrire:
            couleur_ecrire.write(str(carte.get_background_color()))
        with open("Parties" + os.sep + "ombres.sav", "wb") as ombres_ecrire:
            pickle.Pickler(ombres_ecrire).dump(ombrage)
        with open("Parties" + os.sep + "teleporteurs.sav", "wb") as teleport_ecrire:
            pickle.Pickler(teleport_ecrire).dump(teleporteurs)
        with open("Parties" + os.sep + "gamemode.sav", "wb") as creatifmode_ecrire:
            pickle.Pickler(creatifmode_ecrire).dump(creatif)
        with open("Parties" + os.sep + "shader.sav", "wb") as shader_ecrire:
            pickle.Pickler(shader_ecrire).dump(carte.get_curent_shader())
        with open("Parties" + os.sep + "pancartes.sav", "wb") as ecrire_pancartes:
            pickle.Pickler(ecrire_pancartes).dump(pancartes_lst)
        print('Sauvegarde réussie !\n\n')
        if quitte:
            sys.exit()


    def boum_atomique(carte, x, y, max_scrolling):
        carte.remove_bloc(x, y, '0')
        if y - 1 >= 0:
            carte.remove_bloc(x, y - 1, '0')
            if x - 1 >= 0:
                carte.remove_bloc(x - 1, y - 1, '0')
            if x + 1 <= max_scrolling:
                carte.remove_bloc(x + 1, y - 1, '0')
        if x - 1 >= 0:
            carte.remove_bloc(x - 1, y, '0')
        if x - 2 >= 0:
            carte.remove_bloc(x - 2, y, '0')
        if x + 1 <= max_scrolling:
            carte.remove_bloc(x + 1, y, '0')
        if x + 2 <= max_scrolling:
            carte.remove_bloc(x + 2, y, '0')
        if y + 1 <= 20:
            carte.remove_bloc(x, y + 1, '0')
            if x - 1 >= 0:
                carte.remove_bloc(x - 1, y + 1, '0')
            if x + 1 <= max_scrolling:
                carte.remove_bloc(x + 1, y + 1, '0')


    def molette_(s, number_of_case, direction):
        s = [elt for line in s for elt in line]
        if direction == 'bas':
            number_of_case = number_of_case + 1 if number_of_case + 1 <= len(s) - 1 else len(s) - 1
        elif direction == 'haut':
            number_of_case = number_of_case - 1 if number_of_case - 1 >= 0 else 0
        obj_courant = s[number_of_case]

        return obj_courant, number_of_case


    def fps_stp(temps_avant_fps, root, rcenter, font):
        #donc pas de division par zéro :P
        vrais_fps = trunc(((1000 / (time.time() - temps_avant_fps)) / 1000) if time.time() - temps_avant_fps else 300)
        #Titre avec les fps
        titre = "/* FPS : %5i */" % vrais_fps
        pygame.draw.rect(root, (75, 155, 180), (0, rcenter[1] + 360, 115, 20))
        root.blit(font.render(titre, 1, (10, 10, 10)), (4, rcenter[1] + 362))
        pygame.display.flip()


    def souris_ou_t_es(fenetre, arme_h_g):
        x_souris, y_souris = pygame.mouse.get_pos()
        #x_souris = (x_souris // 30) * 30
        #y_souris = (y_souris // 30) * 30
        fenetre.blit(arme_h_g, (x_souris, y_souris))
        pygame.mouse.set_visible(False)
        return (x_souris, y_souris)


    def mettre_eau(carte, cpt_blit_eau, y_blit, x_blit, eau_bruit):
        y_bloque = []
        for i in range(y_blit, 20):
            if carte.get_tile(x_blit, i) == "0":
                if i not in y_bloque:
                    carte.remove_bloc(x_blit, i, '0')
            else:
                y_bloque.append(i)
            cpt_blit_eau += 1
            for j in range(x_blit - cpt_blit_eau, x_blit + cpt_blit_eau):
                if j >= 0 and j <= carte.get_x_len():
                    #pour ne pas dépasser
                    if carte.get_tile(j, i) == "0" and i not in y_bloque:
                        carte.remove_bloc(j, i, 'e')
        eau_bruit.play()


    def s_invent_dd(s, fenetre, img_tous_blocs, bloc_choisi, marteau, blocs, font, tout, obj_survol):
        check = pygame.image.load("Particules" + os.sep + "check_vert.png").convert_alpha()
        vide_choisi = False
        for y_, ligne in enumerate(s):
            for x_, x_s in enumerate(ligne):
                nom_entite = x_s
                if marteau.has_been_2nd_planed(x_s):
                    x_s = x_s[2::]
                if x_s in blocs.list():
                    fenetre.blit(img_tous_blocs[x_s], (x_ * 31 + 52, y_ * 31 + 52))
                    if x_s == bloc_choisi and bloc_choisi != '0':
                        fenetre.blit(check, (x_ * 31 + 52, y_ * 31 + 52))
                    elif x_s == '0' and bloc_choisi == '0' and not vide_choisi:
                        fenetre.blit(check, (x_ * 31 + 52, y_ * 31 + 52))
                        vide_choisi = True
                if tout:
                    if marteau.has_been_2nd_planed(nom_entite):
                        nom_entite = nom_entite[2::]
                    if nom_entite != "0" and nom_entite in blocs.list() and blocs.get(nom_entite) <= 999:
                        #sinon on aura des gros trait blancs tout moches :P
                        nb = font.render("%3i" % blocs.get(nom_entite), 1, (240, 240, 240))
                        fenetre.blit(nb, (52 + x_ * 31, 52 + y_ * 31))
                    elif blocs.get(nom_entite) > 999 and nom_entite != "0" and nom_entite in blocs.list():
                        nb = font.render("N/A", 1, (240, 240, 240))
                        fenetre.blit(nb, (52 + x_ * 31, 52 + y_ * 31))
                else:
                    breaking = False
                    entite = s[y_][x_]
                    if entite == obj_survol and not breaking:
                        if blocs.get(entite) <= 999:
                            nb = font.render(blocs.dict_name()[entite] + " : %3i" % blocs.get(entite), 1, (240, 240, 240))
                            pygame.draw.rect(fenetre, (150, 150, 150), (50 + x_ * 31 + 30, 50 + y_ * 31 + 30, nb.get_size()[0] + 2, nb.get_size()[1] + 2))
                            fenetre.blit(nb, (52 + x_ * 31 + 30, 52 + y_ * 31 + 30))
                            breaking = True
                        elif blocs.get(entite) > 999:
                            nb = font.render(blocs.dict_name()[entite] + " : N/A", 1, (240, 240, 240))
                            pygame.draw.rect(fenetre, (150, 150, 150), (50 + x_ * 31 + 30, 50 + y_ * 31 + 30, nb.get_size()[0] + 2, nb.get_size()[1] + 2))
                            fenetre.blit(nb, (52 + x_ * 31 + 30, 52 + y_ * 31 + 30))
                            breaking = True


    def afficher_degats_pris(fenetre, degats, font, pos_player):
        x = pos_player[0] - 2
        y = pos_player[1] - 30
        fenetre.blit(font.render("-" + str(degats), 1, (208, 6, 6)), (x, y))


    def drag_and_drop_invent(fenetre, font, blocs, img_tous_blocs, s, root, nb_blocs_large,
                             obj_envoie, x_y, arme_h_g, center, liste_monstres, peacefull,
                             max_scrolling, marteau, carte):
        continue3, clic = 1, 0
        s = s
        obj_pris, obj_avant = "", ""
        obj_retour_actu = obj_envoie
        obj_survol = ""
        last_x, last_y = 0, 0
        #affichage du curseur de la souris
        pygame.mouse.set_visible(True)

        tout = False

        structure_niveau = carte.get_list()

        petits_blocs = img_tous_blocs[1]
        img_tous_blocs = img_tous_blocs[0]

        liste_innafichable_dad = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'c', '/§', '§%', 'Q', 'S']

        #carte affichage type bandeau / reader-like
        numero_niv = carte.get_fov()[0]
        var_niv_monstres = "Il peut y avoir des monstres aux niveaux "
        decalage_x = 0
        slice_ = [0, 54]
        structure = structure_niveau
        center_screen = (600 - 250) // 2
        center_x = taille_fenetre_largeur_win // 2 - 580 // 2 + 740 // 2 - 10
        inventaire = pygame.image.load("Fond" + os.sep + "inventaire.png").convert_alpha()
        carte_img = pygame.image.load("Fond" + os.sep + "carte.png").convert_alpha()

        while continue3:
            #le temps pour calculer les FPS !
            temps_avant_fps = time.time()

            carte.render()

            #on dessine le fond (et accessoirement on efface ainsi la fenetre) :
            fenetre.blit(inventaire, (10, 10))

            #carte
            fenetre.blit(carte_img, (center_x - 16, center_screen - 8))
            fenetre.blit(font2.render("*-* Carte *-*", 1, (220, 220, 220)), (center_x + 580 // 2 - 40, center_screen))
            carte_miniature = [line[slice_[0]:slice_[1]] for line in structure]
            for y_ in range(20):
                for x_ in range(len(carte_miniature[0])):
                    case = carte_miniature[y_][x_]
                    case = case if not marteau.has_been_2nd_planed(case) else case[2::]
                    if case not in liste_innafichable_dad:
                        fenetre.blit(petits_blocs[case], ((x_ * 10) + center_x + 10,
                                                            (y_ * 10) + center_screen + 30))
                    elif case == '0':
                        pygame.draw.rect(fenetre, (30, 150, 205), (x_ * 10 + center_x + 10,
                                                                   y_ * 10 + center_screen + 30,
                                                                   10, 10))
                    else:
                        pygame.draw.rect(fenetre, (250, 150, 205), (x_ * 10 + center_x + 10,
                                                                   y_ * 10 + center_screen + 30,
                                                                   10, 10))

            #et on met les icones et leur quantité !
            s_invent_dd(s, fenetre, img_tous_blocs, obj_retour_actu, marteau, blocs, font, tout, obj_survol)

            #et enfin on laisse TOUT LE TEMPS le bloc suivre la souris, si y en a un ;)
            x_souris, y_souris = souris_ou_t_es(fenetre, arme_h_g)

            if obj_pris != "":
                #y a un bloc qui doit suivre la souris !
                fenetre.blit(img_tous_blocs[obj_pris], (x_souris, y_souris))

            #gestion des events
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 \
                                and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_pris = s[yi][xi]
                            last_x, last_y = xi, yi
                            s[yi][xi] = "0"  #on vide la case !
                        clic = 1  #clic actif
                    elif event.button == 3:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 \
                                and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_retour_actu = s[yi][xi]
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 \
                                and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8 \
                                and obj_pris != "":
                            obj_avant = s[yi][xi]
                            s[last_y][last_x] = obj_avant
                            s[yi][xi] = obj_pris
                            obj_retour_actu = obj_pris
                            obj_pris = ""
                            clic = 0  #clic non actif
                        else:
                            s[last_y][last_x] = obj_pris
                            obj_pris = ""
                            clic = 0  #clic non actif
                    elif event.button == 3:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 \
                                and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_retour_actu = s[yi][xi]
                elif event.type == MOUSEMOTION:
                    xi = event.pos[0]
                    yi = event.pos[1]
                    if clic and obj_pris != "":
                        #déplacement car clic est ok, bouton gauche enfoncé (ou droit)
                        #faut que le bloc suive la souris !
                        fenetre.blit(img_tous_blocs[obj_pris], (xi, yi))
                    else:
                        if xi >= 52 and xi <= 52 + 31 * 16 and yi >= 52 and yi <= 52 + 31 * 8:
                            yi_selec = (yi - 52) // 31
                            xi_selc = (xi - 52) // 31
                            if 0 <= yi_selec <= len(s) - 1 and 0 <= xi_selc <= len(s[0]) - 1:
                                obj_survol = s[yi_selec][xi_selc]
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if slice_[1] + 5 <= 5000:
                            slice_[0] += 5
                            slice_[1] += 5
                    elif event.key == K_LEFT:
                        if slice_[0] - 5 >= 0:
                            slice_[0] -= 5
                            slice_[1] -= 5
                    elif event.key == K_PRINT:
                        continuer = 1
                    else:
                        continue3 = 0

            if not peacefull:
                message_affiche_non_bloquant("Vous êtes actuellement dans la section : " + str(numero_niv) + "/" + str(
                    max_scrolling) + ".\n" + var_niv_monstres + str(liste_monstres[0]) + ", " \
                                + str(liste_monstres[1]) + ", " + str(liste_monstres[2]) + " et " + str(
                    liste_monstres[3]) + " !", rcenter)
            elif peacefull:
                message_affiche_non_bloquant("Vous êtes actuellement dans la section : " + str(numero_niv) + "/" + str(
                    max_scrolling) + ".", rcenter)

            pygame.display.flip()
            #actualisation des FPS:
            fps_stp(temps_avant_fps, root, rcenter, font)
        if obj_retour_actu != "":
            return obj_retour_actu, s
        else:
            return obj_envoie, s


    def custom(root_, rcenter, font, creatif, volume_son_j):
        #modification du "launcher"
        pygame.draw.rect(root_, (0, 0, 0), (rcenter[0] - 20, 9, 200, 17))
        #textes
        root_.blit(font.render("Créatif (Off - On)", 1, (255, 255, 255)), (rcenter[0] - 10, 12))
        #boutons
        pygame.draw.rect(root_, (140, 140, 140), (rcenter[0] + 120, 9, 43, 17))
        if creatif:
            pygame.draw.rect(root_, (140, 140, 140), (rcenter[0] + 120, 10, 43, 15))
            pygame.draw.rect(root_, (180, 20, 20), (rcenter[0] + 120 + 1, 10, 20, 15))
        elif not creatif:
            pygame.draw.rect(root_, (140, 140, 140), (rcenter[0] + 120, 10, 43, 15))
            pygame.draw.rect(root_, (20, 180, 20), (rcenter[0] + 120 + 22, 10, 20, 15))
        #actualisation de l'écran pour afficher les changements
        pygame.display.flip()


    def aff_bloc(root, obj_courant, img_tous_blocs, rcenter, inventaire_blocs_list, nom_tous_blocs, font, blocs_):
        liste_ordre_invent = []
        pos_bloc = 0
        for ligne in inventaire_blocs_list:
            for element in ligne:
                liste_ordre_invent.append(element)
        for x, case in enumerate(liste_ordre_invent):
            if case == obj_courant:
                pos_bloc = x
        liste_ordre_invent = liste_ordre_invent[pos_bloc:pos_bloc+9]
        centrage = taille_fenetre_largeur_win // 2 - (9 * (34 + 2)) // 2
        for nombre, bloc in enumerate(liste_ordre_invent):
            if bloc != obj_courant:
                pygame.draw.rect(root, (140, 140, 140), (centrage + nombre * 36, rcenter[1] + 310, 34, 34))
            elif bloc == obj_courant:
                pygame.draw.rect(root, (0, 0, 0), (centrage + nombre * 36, rcenter[1] + 310 + 30 + 4, 300, 30))
                root.blit(font.render(nom_tous_blocs[bloc] + " : " + str(blocs_.get(bloc)), 1,
                                      (255, 255, 255), (0, 0, 0)),
                                      (centrage + nombre * 36, rcenter[1] + 310 + 30 + 4))
                pygame.draw.rect(root, (41, 235, 20), (centrage + nombre * 36, rcenter[1] + 310, 34, 34))
            root.blit(img_tous_blocs[bloc], (centrage + nombre * 36 + 2, rcenter[1] + 310 + 2))


    def flash(fenetre, carte):
        pygame.draw.rect(fenetre, (240, 240, 240),
                         (0, 0, taille_fenetre_largeur_win, 600))
        pygame.display.flip()
        pygame.time.wait(time_flash)
        carte.render()
        pygame.display.flip()


    def padding_0(liste):
        intermediaire = []
        for i in liste:
            temp = str(int(i[21::].split('.')[0]))
            intermediaire.append('0' * (4 - len(temp)) + str(temp))
        intermediaire.sort()
        return intermediaire


    def time_cruise(fenetre, largeur_dispo, font, arme_h_g, carte, personnage):
        vieille_carte = None
        field_of_view_chose = 0
        width_ = 500
        height_ = 450
        continuer = 1
        liste_cartes = [i for i in glob.glob("Niveaux" + os.sep + "Olds Maps" + os.sep + "*.lvl")]
        liste_cartes_originelles = liste_cartes
        liste_cartes = padding_0(liste_cartes)
        choisi = -1

        while continuer:
            carte.render()
            pygame.draw.rect(fenetre, couleur_idd, ((largeur_dispo - width_) // 2,
                                                  300 - (height_ // 2),
                                                  width_,
                                                  height_))
            for i in range(len(liste_cartes)):
                if 300 - (height_ // 2) <= 310 - (height_ // 2) + i * 32 + field_of_view_chose <= height_ + 268 - (height_ // 2):
                    if choisi == i:
                        pygame.draw.rect(fenetre, (85, 215, 45), ((largeur_dispo - width_) // 2 + 10,
                                                            310 - (height_ // 2) + i * 32 + field_of_view_chose,
                                                            width_ - 10 * 2, 30))
                    else:
                        pygame.draw.rect(fenetre, (45, 175, 190), ((largeur_dispo - width_) // 2 + 10,
                                                            310 - (height_ // 2) + i * 32 + field_of_view_chose,
                                                            width_ - 10 * 2, 30))
            for i, j in enumerate(liste_cartes):
                nom_destination = ('Année ' + j).replace(' 0', ' ').replace(' 0', ' ').replace(' 0', ' ')
                if 300 - (height_ // 2) <= 310 - (height_ // 2) + i * 32 + field_of_view_chose <= height_ + 268 - (height_ // 2):
                    fenetre.blit(font.render(nom_destination, 1, (10, 10, 10)),
                                 ((largeur_dispo - width_) // 2 + 10,
                                 310 - (height_ // 2) + i * 32 + field_of_view_chose))

            pygame.draw.rect(fenetre, (85, 215, 45), ((largeur_dispo - width_) // 2 + 10,
                                                      310 + height_ // 2 - 40,
                                                      35, 20))

            x_s, x_s1 = souris_ou_t_es(fenetre, arme_h_g)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        continuer = 0
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        #molette UP
                        field_of_view_chose += 32
                    elif event.button == 5:
                        #molette DOWN
                        field_of_view_chose -= 32
                    elif event.button == 1:
                        #clic LEFT
                        if (largeur_dispo - width_) // 2 + 10 <= x_s <= (largeur_dispo - width_) // 2 + 10 + 35 \
                                and 310 + height_ // 2 - 40 <= x_s1 <= 310 + height_ // 2 - 20:
                            continuer = 0
                        elif (largeur_dispo - width_) // 2 <= x_s <= (largeur_dispo - width_) // 2 + width_:
                            choisi = (x_s1 - (310 - (height_ // 2) + field_of_view_chose)) // 32
            pygame.display.flip()

        if choisi != -1 and 0 <= choisi <= len(liste_cartes) - 1:
            carte.load(liste_cartes_originelles[choisi])
            flash(fenetre, carte)

        personnage.set_y(0)

        return choisi


    def reseau_speaking(socket, message, params, personnage, carte, blocs_):
        if message[:4] != 'tp->' and message[:6] != "give->" and message[:5] != "ban->" \
                and message[:9] != "upgrade->" and message[:8] != "season->":
            requete = "set->chat" + message
            socket.sendto(pickle.dumps(requete), params)
        elif message[:6] == "give->":
            temp = message[:6].split(',')
            personne = temp[0]
            bloc = temp[1]
            quantity = temp[2]
            if bloc in blocs_.list():
                if quantity <= blocs_.get(bloc):
                    blocs_.use(bloc, nbr=quantity)
            ############################################ non terminée
        elif message[:5] == "ban->" or message[:9] == 'upgrade->':
            socket.sendto(pickle.dumps(message), params)


    def reseau_define_mypos(socket, mypos, params):
        socket.sendto(pickle.dumps("set->pos" + str(mypos[0]) + ":" + str(mypos[1]) + ":" + mypos[2]), params)


    def actualise_chat(s, params, surface, font):
        s.sendto(pickle.dumps("get->chat"), params)
        temp = s.recv(4096)
        temp = pickle.loads(temp)
        surf = pygame.Surface((420, 22 * 6))
        surf.fill(0x000000)
        surf.set_alpha(60)
        surf.convert_alpha()
        surface.blit(surf, (surface.get_size()[0] - 430, surface.get_size()[1] - surf.get_size()[1] - 10))
        for i in range(len(temp)):
            msg = temp[i][0]
            color = temp[i][1]
            rendu = font.render(msg, 1, color)
            surface.blit(rendu, (surface.get_size()[0] - 420, i * rendu.get_size()[1] + (surface.get_size()[1] - surf.get_size()[1] - 10)))


    pygame.joystick.init()
    joystick_player = pygame.joystick.get_count()
    if joystick_player:
        print("Un joystick est connecté !")
        mon_joystick = pygame.joystick.Joystick(0)
        mon_joystick.init()  #Initialisation
        print("Axes :", mon_joystick.get_numaxes())
        print("Boutons :", mon_joystick.get_numbuttons())
        print("Trackballs :", mon_joystick.get_numballs())
        print("Hats :", mon_joystick.get_numhats())

    if os.path.exists("Parties" + os.sep + "equipement_en_cours.sav") \
            and os.path.exists("Parties" + os.sep + "niveau.sav") and os.path.exists(
                            "Parties" + os.sep + "bloc.sav") \
            and os.path.exists("Parties" + os.sep + "pos.sav") and os.path.exists(
                            'Parties' + os.sep + "fov.sav") \
            and os.path.exists('Parties' + os.sep + 'mana.sav') and os.path.exists(
                            'Parties' + os.sep + 'couleur.sav') \
            and os.path.exists('Parties' + os.sep + 'ombres.sav') and os.path.exists(
                            'Parties' + os.sep + 'teleporteurs.sav') \
            and os.path.exists('Parties' + os.sep + "gamemode.sav") and os.path.exists(
                            'Parties' + os.sep + 'shader.sav') \
            and os.path.exists('Parties' + os.sep + 'pancartes.sav'):
        load_texte = "Chargement des fichiers . . .\n"
        with open('Parties' + os.sep + 'equipement_en_cours.sav', 'rb') as lire_equipement:
            obj_courant = pickle.Unpickler(lire_equipement).load()
            number_of_case = {v: k for k, v in enumerate([elt for line in lst_inventaire for elt in line])}[obj_courant]
            load_texte = "\nequipement_en_cours.sav >>> Chargé !\n"
            print(load_texte)
        with open("Parties" + os.sep + "bloc.sav", "rb") as bloc_lire:
            blocs = pickle.Unpickler(bloc_lire).load()
            load_texte = "bloc.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'niveau.sav', 'rb') as niv_lire:
            numero_niv = pickle.Unpickler(niv_lire).load()
            load_texte = "niveau.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'pos.sav', 'rb') as pos_lire:
            personnage.set_pos(pickle.Unpickler(pos_lire).load())
            load_texte = "pos.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'fov.sav', 'rb') as fov_lire:
            temp = pickle.Unpickler(fov_lire).load()
            carte.set_fov(temp[0], temp[1])
            load_texte = "fov.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'mana.sav', 'rb') as mana_lire:
            personnage.set_mana(pickle.Unpickler(mana_lire).load())
            load_texte = "mana.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'ombres.sav', 'rb') as ombres_lire:
            ombrage = pickle.Unpickler(ombres_lire).load()
            load_texte = "ombres.sav >>> Chargé !\n"
            print(load_texte)
        with open('Parties' + os.sep + 'teleporteurs.sav', 'rb') as telep_lire:
            liste_teleporteurs = pickle.Unpickler(telep_lire).load()
            load_texte = "teleporteurs.sav >>> Chargé !\n"
            print(load_texte)
        with open("Parties" + os.sep + "gamemode.sav", "rb") as creatifmode_lire:
            creatif = pickle.Unpickler(creatifmode_lire).load()
            load_texte = "gamemode.sav >>> Chargé !\n"
            print(load_texte)
        with open("Parties" + os.sep + "shader.sav", "rb") as shader_lire:
            carte.set_current_shader(pickle.Unpickler(shader_lire).load())
            load_texte = "shader.sav >>> Chargé !\n"
            print(load_texte)
        with open("Parties" + os.sep + "pancartes.sav", "rb") as lire_pancartes:
            pancartes_lst = pickle.Unpickler(lire_pancartes).load()
            load_texte = "pancartes.sav >>> Chargé !\n"
            print(load_texte)
        with open("Parties" + os.sep + "couleur.sav", "r") as clr:
            carte.set_background_color(eval(clr.read()))
            load_texte = "couleur.sav >>> Chargé !\n"
            print(load_texte)
    if os.path.exists('Parties' + os.sep + 'texture_pack.sav'):
        with open('Parties' + os.sep + 'texture_pack.sav', 'r') as txtpr:
            texture_pack_path = txtpr.read()
    if os.path.exists('Parties' + os.sep + 'jheight.sav'):
        with open('Parties' + os.sep + 'jheight.sav', 'r') as jhr:
            jump_height = int(jhr.read())
        liste_hauteur_saut = [-1 for _ in range(jump_height + 1)] + [+1 for _ in range(jump_height + 2)]
    if os.path.exists('Parties' + os.sep + 'jtime.sav'):
        with open('Parties' + os.sep + 'jtime.sav', 'r') as tjr:
            temps_saut_attendre = int(tjr.read()) / 1000

    if not os.path.exists('Parties' + os.sep + 'pos.sav'):
        #création de nouveau fichiers
        message_affiche_large(grd_msg_bjr, fenetre, rcenter)

    #on charge les sprites
    carte.load_image()

    #actualisation de l'écran
    pygame.display.flip()
    #activation de la répétition des touches
    pygame.key.set_repeat(200, personnage.get_speed())
    #on n'affiche pas le curseur de la souris !
    pygame.mouse.set_visible(False)

    #si on est en créatif, on a tout les blocs en *9999 !
    if not creatif or vip_bool:
        #on est encore et quand même en créatif :D
        for index in blocs.list():
            if blocs.get(index) < 900 and index not in ('bn', 'n?', '?.', '/§', '§%'):
                quant = 5000 if not creatif else blocs.get(index) + 150
                blocs.set(index, nbr=quant)

    #vie
    personnage.afficher_vie()
    #affichage de la mana
    personnage.afficher_mana()

    last_music_time = time.time() + 30  #secondes

    FPS = cst.IAFPS(75)
    cpt_tour = 0
    tps_tour = time.time() + 1

    if en_reseau:
        socket_client_serv.sendto(pickle.dumps("get->configuration"), params_co)
        data_serv = []
        with open("Parties" + os.sep + "serveur.sav", "rb+") as data_serv_wrb:
            data_serv = pickle.Unpickler(data_serv_wrb).load()
            temp = socket_client_serv.recv(4096)
            temp = pickle.loads(temp)
            for i in range(len(data_serv)):
                if data_serv[i][0] == str(hote) + ':' + str(port):
                    data_serv[i][1] = temp[0]
                    data_serv[i][2] = temp[1]
                    break
            pickle.Pickler(data_serv_wrb).dump(data_serv)
        with open("Parties" + os.sep + "serveur.sav", "wb") as f:
            pickle.Pickler(f).dump(data_serv)

    while continuer:
        temps_avant_fps = time.time()

        #gestion des shaders gourmants:
        if carte.get_curent_shader() == 'gaussien' or carte.get_curent_shader() == 'progressif':
            FPS.set_FPS(200)
        else:
            FPS.default()
        #le "tour" de l'ecran de jeu
        custom(root, rcenter, font, creatif, volume_son_j)
        #les "last"
        last_pos = (personnage.get_pos()[0] - 30, personnage.get_pos()[1]) if situation_actuelle == 'droite' else (personnage.get_pos()[0] + 30, personnage.get_pos()[1])
        #la carte réseau
        if en_reseau:
            carte.receive_map()
            carte.make_choice_oth(affiche_oth)
            reseau_define_mypos(socket_client_serv,
                                [personnage.get_pos()[0] // 30 + carte.get_fov()[0],
                                 personnage.get_pos()[1] // 30, situation_actuelle],
                                params_co)
        #la gravité pour les entités
        carte.gravity_for_entity()
        #destruction des bombes atomiques non bloquantes
        iBList = 0
        while iBList <= len(boumList) - 1:
            item = boumList[iBList]
            if time.time() - item[0] > 2:
                boum_atomique(carte, item[1][0], item[1][1], max_scrolling)
                boumList.pop(iBList)
            iBList += 1
        #destruction des blocs non bloquant
        iBreakList = 0
        while iBreakList <= len(breakListe) - 1:
            item = breakListe[iBreakList]
            if time.time() - item[4] > item[3]:
                carte.remove_bloc(item[0], item[1], item[2])
                breakListe.pop(iBreakList)
                breaking_bloc.play()
            iBreakList += 1
        #rendu de la carte et de la meteo
        carte.render()

        #vie & mana
        if show_stats:
            personnage.afficher_vie()
            personnage.afficher_mana()
            marteau.render()
        #régénration de la mana
        personnage.regen_mana()

        x_s, x_s1 = souris_ou_t_es(fenetre, arme_h_g)

        #gestion des évenements
        for evennements_fenetre in [pygame.event.poll()]:
            #gestion des évenements
            #controle pour quitter
            if evennements_fenetre.type == KEYDOWN and (
                            evennements_fenetre.key == K_ESCAPE or evennements_fenetre.key == K_F4):
                carte.save()
                with open('s.sav', 'wb') as save_idd:
                    pickler_10 = pickle.Pickler(save_idd)
                    pickler_10.dump(lst_inventaire)
                sauvegarder(False, personnage, obj_courant, ombrage, liste_teleporteurs, creatif, pancartes_lst, carte)
                continuer = 0
            elif evennements_fenetre.type == QUIT and windowed_is:
                carte.save()
                with open('s.sav', 'wb') as save_idd:
                    pickler_10 = pickle.Pickler(save_idd)
                    pickler_10.dump(lst_inventaire)
                sauvegarder(True, personnage, obj_courant, ombrage, liste_teleporteurs, creatif, pancartes_lst, carte)
            #controles autour de la souris
            elif evennements_fenetre.type == MOUSEBUTTONDOWN:
                if evennements_fenetre.button == 5:  #la molette descend
                    obj_courant, number_of_case = molette_(lst_inventaire, number_of_case, 'bas')
                elif evennements_fenetre.button == 4:  #la molette monte
                    obj_courant, number_of_case = molette_(lst_inventaire, number_of_case, 'haut')
                elif evennements_fenetre.button == 1:
                    clique_gauche = 1
                    #clic, donc on pose un bloc là où on a cliqué !
                    x_blit = evennements_fenetre.pos[0] // 30 + carte.get_fov()[0]
                    y_blit = evennements_fenetre.pos[1] // 30
                    if y_blit <= 19 and x_blit <= max_scrolling - 1 and (blocs.get(obj_courant) > 0 or not creatif) \
                            and ((x_blit, y_blit) != (personnage.get_pos()[0] // 30 + carte.get_fov()[0], personnage.get_pos()[1] // 30) or obj_courant not in blocs.list_solid()) \
                            and obj_courant not in blocs.list_unprintable():
                        if carte.get_tile(x_blit, y_blit) not in blocs.list_unprintable():
                            if not creatif: #on est quand meme en créatif x)
                                carte.remove_bloc(x_blit, y_blit, obj_courant)
                            if creatif:
                                #"temps" de destruction d'un bloc
                                if marteau.has_been_2nd_planed(carte.get_tile(x_blit, y_blit)):
                                    #item: #0 : x #1 : y #2 : nouveau bloc #3 : temps #4 : heure de la pose
                                    breakListe.append([x_blit, y_blit, obj_courant, blocs.get_time(carte.get_tile(x_blit, y_blit)[2::]) // 100, time.time()])
                                else:
                                    #item: #0 : x #1 : y #2 : nouveau bloc #3 : temps #4 : heure de la pose
                                    breakListe.append([x_blit, y_blit, obj_courant, blocs.get_time(carte.get_tile(x_blit, y_blit)[2::]) // 100, time.time()])
                            if carte.get_tile(x_blit, y_blit) in list(blocs.list()) and creatif: #si on est pas en creatif
                                #le bloc existe, on met 1 bloc en plus dans l'inventaire
                                if marteau.has_been_2nd_planed(carte.get_tile(x_blit, y_blit)):
                                    blocs.set(carte.get_tile(x_blit, y_blit)[2::], nbr=blocs.get(carte.get_tile(x_blit, y_blit)[2::])+1)
                                else:
                                    blocs.set(carte.get_tile(x_blit, y_blit), nbr=blocs.get(carte.get_tile(x_blit, y_blit))+1)
                            elif carte.get_tile(x_blit, y_blit) in blocs.list() and creatif:
                                #le bloc n'existe pas dans l'inventaire, on l'ajoute donc
                                blocs.add(carte.get_tile(x_blit, y_blit), solid=True, shadow=0, gravity=False, quantity=1, innafichable=False, name='No name', tps_explode=0, take_fire=False)
                            #on enlève 1 pour le bloc POSé:
                            if blocs.get(obj_courant) - 1 >= 0 and creatif:
                                blocs.use(obj_courant)
                            if obj_courant == 'vb':
                                #téléporteur
                                if not en_reseau:
                                    liste_teleporteurs.append([len(liste_teleporteurs), (x_blit, y_blit)])
                                else:
                                    socket_client_serv.sendto(pickle.dumps('set->telep' + str(x_blit) + ',' + str(y_blit)), params_co)
                            if obj_courant == '%a':
                                #pancartes
                                if not en_reseau:
                                    pancartes_lst.append([(x_blit, y_blit), ''])
                                else:
                                    socket_client_serv.sendto(pickle.dumps("set->pan" + str(x_blit) + "," + str(y_blit)), params_co)
                            if carte.get_tile(x_blit, y_blit) == '%a' and obj_courant != '%a':
                                #on casse une pancarte
                                if not en_reseau:
                                    #on doit donc liberer la place pour ne pas perdre en espace disque
                                    for i in range(len(pancartes_lst)):
                                        if pancartes_lst[i][0] == (x_blit, y_blit):
                                            pancartes_lst.pop(i)
                                            break
                                else:
                                    socket_client_serv.sendto(pickle.dumps("break->pan" + str(x_blit) + "," + str(y_blit)), params_co)
                            if carte.get_tile(x_blit, y_blit) == 'vb' and obj_courant != 'vb':
                                #on casse un téléporteur
                                if not en_reseau:
                                    #oui oui, en mode réseau, on ne peut pas casser de téléporteurs :D
                                    for i in range(len(liste_teleporteurs)):
                                        if liste_teleporteurs[i][1] == (x_blit, y_blit):
                                            if liste_teleporteurs[i][0] % 2:
                                                #impair
                                                carte.remove_bloc(liste_teleporteurs[i][1][0], liste_teleporteurs[i][1][1], '0')
                                                carte.remove_bloc(liste_teleporteurs[i - 1][1][0], liste_teleporteurs[i - 1][1][1], '0')
                                                liste_teleporteurs.pop(i)
                                                liste_teleporteurs.pop(i - 1)
                                            elif not liste_teleporteurs[i][0] % 2:
                                                #pair
                                                if not len(liste_teleporteurs) % 2:
                                                    #la longueur est paire, alors un autre téléporteur est associé a celui ci
                                                    #et on doit donc aussi le casser
                                                    carte.remove_bloc(liste_teleporteurs[i + 1][1][0], liste_teleporteurs[i + 1][1][1], '0')
                                                    carte.remove_bloc(liste_teleporteurs[i][1][0], liste_teleporteurs[i][1][1], '0')
                                                    liste_teleporteurs.pop(i + 1)
                                                    liste_teleporteurs.pop(i)
                            if obj_courant == 'e':
                                #eau
                                carte.remove(x_blit, y_blit, "e")
                                if carte.get_tile(x_blit, y_blit) == "e":
                                    cpt_blit_eau = 0
                                    #i = y_blit
                                    #j = x_blit
                                    mettre_eau(carte, cpt_blit_eau, y_blit, x_blit, eau_bruit)
                elif evennements_fenetre.button == 3 and (obj_courant not in blocs.list_unprintable() or
                                                                  obj_courant == '§%' or obj_courant in dico_cd.keys()):
                    x_clic = evennements_fenetre.pos[0] // 30 + carte.get_fov()[0]
                    y_clic = evennements_fenetre.pos[1] // 30
                    if carte.get_tile(x_clic, y_clic) == 'cv':
                        #bombe atomique
                        boumList.append([time.time(),(x_clic,y_clic)])
                    elif carte.get_tile(x_clic, y_clic) == 'vb':
                        #on veut se téléporter
                        if not en_reseau:
                            for i in range(len(liste_teleporteurs)):
                                if liste_teleporteurs[i][1] == (x_clic, y_clic):
                                    if liste_teleporteurs[i][0] % 2:
                                        #impair
                                        #passage en cases
                                        z = liste_teleporteurs[i - 1][1][0] - (personnage.get_pos()[0] // 30 + carte.get_fov()[0])
                                        if carte.get_fov()[0] + z <= max_scrolling - carte.get_space():
                                            carte.set_fov(carte.get_fov()[0] + z, carte.get_fov()[1] + z)
                                        else:
                                            carte.set_fov(max_scrolling - carte.get_space(), max_scrolling)
                                        #personnage.set_x(liste_teleporteurs[i - 1][1][0]) * 30
                                        personnage.set_y((liste_teleporteurs[i - 1][1][1] - 1 if y_clic - 1 >= 0 else liste_teleporteurs[i - 1][1][1] + 1) * 30)
                                        #pour etre au dessus et pas dedans
                                    elif not liste_teleporteurs[i][0] % 2:
                                        #pair
                                        if not len(liste_teleporteurs) % 2:
                                            #passage en cases
                                            z = liste_teleporteurs[i + 1][1][0] - (personnage.get_pos()[0] // 30 + carte.get_fov()[0])
                                            if carte.get_fov()[0] + z <= max_scrolling - carte.get_space():
                                                carte.set_fov(carte.get_fov()[0] + z, carte.get_fov()[1] + z)
                                            else:
                                                carte.set_fov(max_scrolling - carte.get_space(), max_scrolling)
                                            personnage.set_y((liste_teleporteurs[i + 1][1][1] - 1 if y_clic - 1 >= 0 else liste_teleporteurs[i + 1][1][1] + 1) * 30)
                                        elif len(liste_teleporteurs) % 2 and i == len(liste_teleporteurs) - 1:
                                            message_affiche("Aucune cible n'a été définie pour ce téléporteur !", rcenter)
                        else:
                            socket_client_serv.sendto(pickle.dumps('get->telep' + str(x_clic) + ',' + str(y_clic)), params_co)
                            temp = socket_client_serv.recv(4096)
                            temp = pickle.loads(temp)
                            #passage en cases
                            z = temp[0] - (personnage.get_pos()[0] // 30 + carte.get_fov()[0])
                            if carte.get_fov()[0] + z <= max_scrolling - carte.get_space():
                                carte.set_fov(carte.get_fov()[0] + z, carte.get_fov()[1] + z)
                            else:
                                carte.set_fov(max_scrolling - carte.get_space(), max_scrolling)
                            personnage.set_y((temp[1] - 1 if y_clic - 1 >= 0 else temp[1] + 1) * 30)
                            #pour etre au dessus et pas dedans
                    elif obj_courant in dico_cd.keys() and carte.get_tile(x_clic, y_clic) == 'B':
                        #jukebox
                        indice_son = 0 if obj_courant == 'qs' else 1
                        indice_son = 1 if obj_courant == 'sd' else 2
                        indice_son = 2 if obj_courant == 'df' else 3
                        if not pygame.mixer.music.get_busy():
                            last_cd_used = obj_courant
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                            blocs.set(last_cd_used, nbr=blocs.get(last_cd_used)+1)
                        pygame.mixer.music.load(music_liste[indice_son])
                        pygame.mixer.music.play()
                    elif obj_courant == '§%' and carte.get_tile(x_clic, y_clic) != '0':
                        marteau.utiliser(carte, y_clic, x_clic)
                    elif carte.get_tile(x_clic, y_clic) == '%a':
                        if not en_reseau:
                            for i in pancartes_lst:
                                if i[0] == (x_clic, y_clic):
                                    if i[1] != '':
                                        message_affiche(i[1], rcenter)
                                    else:
                                        i[1] = dlb.DialogBox(fenetre, 'Entrez votre texte :', 'Edition d\'une pancarte',
                                                             rcenter, grd_font, y_ecart, type_btn=2, mouse=True, carte=carte).render()
                                    break
                        else:
                            socket_client_serv.sendto(pickle.dumps("get->pan" + str(x_clic) + "," + str(y_clic)), params_co)
                            temp = socket_client_serv.recv(4096)
                            temp = pickle.loads(temp)
                            if not temp:
                                texte_pan_to_send = dlb.DialogBox(fenetre, 'Entrez votre texte :', 'Edition d\'une pancarte',
                                                                  rcenter, grd_font, y_ecart, type_btn=2, mouse=True, carte=carte).render()
                                socket_client_serv.sendto(pickle.dumps("set->pan" + str(x_clic) + "," + str(y_clic) + "," + texte_pan_to_send), params_co)
                            else:
                                message_affiche(temp, rcenter)
                    elif carte.get_tile(x_clic, y_clic) == '%b':
                        if not en_reseau:
                            annee = time_cruise(fenetre, fenetre.get_size()[0], font, arme_h_g, carte, personnage)
                        else:
                            message_affiche("Vous ne pouvez pas voyager dans le temps en mode réseau", rcenter)
            elif evennements_fenetre.type == MOUSEBUTTONUP:
                if evennements_fenetre.button == 1:
                    #clic gauche
                    #on relache la souris donc on met à false le 'booleen' qui dit que l'on peut
                    clique_gauche = 0
                    #maj de l'écran
                    pygame.display.flip()
                elif evennements_fenetre.button == 3:
                    #clique droit
                    if obj_courant in blocs.list_unprintable():
                        #on enlève 1 potion
                        if obj_courant not in liste_septre and obj_courant not in dico_cd.keys() and obj_courant not in ('§%'):
                            blocs.use(obj_courant)
                        if obj_courant == 'Q':
                            personnage.update_vie(100)
                        elif obj_courant == 'S':
                            personnage.update_mana(100)
                        elif obj_courant in liste_septre:
                            personnage.mana_action(creatif, obj_courant, evennements_fenetre.pos)
                elif evennements_fenetre.button == 2:  #bouton du milieu (molette de la souris)
                    #on a récupéré le bloc et on l'a affecté comme bloc en cours d'utilisation
                    obj_courant = carte.get_tile((evennements_fenetre.pos[0] // 30) + carte.get_fov()[0], (evennements_fenetre.pos[1] // 30))
            elif evennements_fenetre.type == MOUSEMOTION:
                if clique_gauche and not creatif:  #en fait on est en créatif quand meme dans ce cas ci :)
                    x_blit = evennements_fenetre.pos[0] // 30 + carte.get_fov()[0]
                    y_blit = evennements_fenetre.pos[1] // 30
                    if y_blit <= 19 and x_blit <= max_scrolling and blocs.get(obj_courant) > 0 \
                            and ((x_blit, y_blit) != (
                                            personnage.get_pos()[0] // 30 + carte.get_fov()[0],
                                            personnage.get_pos()[1] // 30) or obj_courant not in blocs.list_solid()):
                        if carte.get_tile(x_blit, y_blit) not in blocs.list_unprintable():
                            if carte.get_tile(x_blit, y_blit) in blocs.list() and creatif:
                                #donc si on est en créatif, on ajoute pas
                                #le bloc existe, on met 1 bloc en plus dans l'inventaire
                                #mais on vérifie avant qu'il n'est pas en arriere plan, sans quoi
                                #l'affichage dans l'inventaire ne fonctionnera pas !
                                if marteau.has_been_2nd_planed(carte.get_tile(x_blit, y_blit)):
                                    blocs.set(carte.get_tile(x_blit, y_blit)[2::], nbr=blocs.get(carte.get_tile(x_blit, y_blit)[2::])+1)
                                else:
                                    blocs.set(carte.get_tile(x_blit, y_blit), nbr=blocs.get(carte.get_tile(x_blit, y_blit))+1)
                            elif creatif and carte.get_tile(x_blit, y_blit) not in blocs.list():
                                #le bloc n'existe pas dans l'inventaire, on l'ajoute donc
                                blocs.add(carte.get_tile(x_blit, y_blit), solid=True, shadow=0, gravity=False, quantity=1, innafichable=False, name='No name', tps_explode=0, take_fire=False)
                            #on enlève 1 pour le bloc POSé:
                            if blocs.get(obj_courant) - 1 >= 0 and creatif:
                                blocs.use(obj_courant)
                            carte.remove_bloc(x_blit, y_blit, obj_courant)
                            #raffraichir la map pour voir le placement multiple :
                            carte.render()
                            if show_stats:
                                personnage.afficher_vie()
                                personnage.afficher_mana()
                                marteau.render()
                            x_s, x_s1 = souris_ou_t_es(fenetre, arme_h_g)
                            cpt_blit_eau = 0
                            #i = y_blit
                            #j = x_blit
                            if obj_courant == 'e':
                                mettre_eau(carte, cpt_blit_eau, y_blit, x_blit, eau_bruit)
                else:
                    carte.render()
                    if show_stats:
                        personnage.afficher_vie()
                        personnage.afficher_mana()
                        marteau.render()
            #controles au clavier
            elif evennements_fenetre.type == KEYDOWN:
                #controles de déplacement au clavier
                if   evennements_fenetre.key == K_UP:
                    #on monte
                    personnage.move("haut")
                elif evennements_fenetre.key == K_DOWN:
                    #on descend mais uniquement si il y a une echelle en dessous de nous
                    if carte.get_tile(personnage.get_pos()[0] // 30 + carte.get_fov()[0], personnage.get_pos()[1] // 30 + 1) == './':
                        personnage.set_y(personnage.get_pos()[1] + 30)
                elif evennements_fenetre.key == K_LEFT:
                    #on va à gauche
                    situation_actuelle = "gauche"
                    personnage.move("gauche")
                    personnage.change_direction(situation_actuelle)
                elif evennements_fenetre.key == K_RIGHT:
                    #on va à droite
                    situation_actuelle = "droite"
                    personnage.move("droite")
                    personnage.change_direction(situation_actuelle)
                #passage fullscreen -> windowed / windowed -> fullscreen
                elif evennements_fenetre.key == K_u:
                    if windowed_is:
                        root = pygame.display.set_mode((0, 0), FULLSCREEN)
                        r = pygame.Rect(0, 0, taille_fenetre_largeur_win,
                                        600)  #definition de la taille de la fenetre de jeu
                        r.center = root.get_rect().center  #centrage de la fenetre par rapport a l'ecran total
                        fenetre = root.subsurface(r)  #definition de la fenetre de jeu
                        pygame.display.update(r)  #mise a jour de la fenetre seulement
                        custom(root, rcenter, font, creatif, volume_son_j)
                        windowed_is = False
                    else:
                        root = pygame.display.set_mode((0, 0))
                        r = pygame.Rect(0, 0, taille_fenetre_largeur_win,
                                        600)  #definition de la taille de la fenetre de jeu
                        r.center = root.get_rect().center  #centrage de la fenetre par rapport a l'ecran total
                        fenetre = root.subsurface(r)  #definition de la fenetre de jeu
                        pygame.display.update(r)  #mise a jour de la fenetre seulement
                        custom(root, rcenter, font, creatif, volume_son_j)
                        pygame.display.set_caption("UrWorld")
                        windowed_is = True
                #changement de la taille du FOV
                elif evennements_fenetre.key == K_e:
                    new_size_fov = dlb.DialogBox(fenetre, ["Entrez la nouvelle taille du", "FOV (entre 0 et " + str(nb_blocs_large) + " ) :"],
                                  "Réglage du FOV", rcenter, grd_font, y_ecart, type_btn=3, carte=carte).render()
                    if new_size_fov.isdigit():
                        carte.set_fov(carte.get_fov()[0], carte.get_fov()[0] + abs(int(new_size_fov)))
                #controles discuter et inventaire
                elif evennements_fenetre.key == K_d:
                    #on parle à la personne la plus proche de soi
                    passant_parle(fenetre, situation_actuelle, personnage, carte.get_list(), blocs.get('/§'), rcenter,
                                  carte.get_img_dict(), carte.get_fov())
                #controle de l'affichage de l'inventaire Drag&Drop
                elif evennements_fenetre.key == K_LSHIFT or evennements_fenetre.key == K_RSHIFT:
                    monstres_ou_pas = [
                        random.randrange(debut + 1, fin + 1),
                        random.randrange(debut + 1, fin + 1),
                        random.randrange(debut + 1, fin + 1),
                        random.randrange(debut + 1, fin + 1)
                    ]
                    obj_courant, lst_inventaire = drag_and_drop_invent(fenetre, font, blocs, [carte.get_img_dict(), niveau_pkg.img_], lst_inventaire,
                                                            root, carte.get_space(), obj_courant, personnage.get_pos(), arme_h_g,
                                                            rcenter, monstres_ou_pas, peacefull, max_scrolling, marteau, carte)
                    number_of_case = {v: k for k, v in enumerate([elt for line in lst_inventaire for elt in line])}[obj_courant]
                #controles son, creatif
                elif evennements_fenetre.key == K_o:
                    if creatif:
                        creatif = False
                        pygame.draw.rect(root, (140, 140, 140), (rcenter[0] + 120, 9, 43, 17))
                        pygame.draw.rect(root, (20, 180, 20), (rcenter[0] + 120 + 1, 10, 20, 15))
                        personnage.set_vie(last_vie)
                    elif not creatif:
                        creatif = True
                        pygame.draw.rect(root, (140, 140, 140), (rcenter[0] + 120, 9, 43, 17))
                        pygame.draw.rect(root, (180, 20, 20), (rcenter[0] + 120 + 22, 10, 20, 15))
                        last_vie = personnage.get_vie()
                        personnage.set_vie(100)
                elif evennements_fenetre.key == K_i:
                    #la musique en pause ou pas !
                    if pygame.music.get_busy():
                        pygame.mixer.music.set_volume(0)
                    elif not pygame.music.get_busy():
                        pygame.mixer.music.set_volume(volume_son_j)
                #on affiche les autres ou pas :D
                elif evennements_fenetre.key == K_p:
                    affiche_oth = not affiche_oth
                elif evennements_fenetre.key == K_y:
                    carte.switch_shader()
                elif evennements_fenetre.key == K_t:
                    show_cursor = not show_cursor
                #saut
                elif evennements_fenetre.key == K_SPACE:
                    saut = True
                    last_perso_saut = personnage.get_pos()
                    time_saut = time.time() + temps_saut_attendre
                #controles choix du bloc par appui de touches
                elif evennements_fenetre.key == K_1 or evennements_fenetre.key == K_KP1:
                    obj_courant = "q"  #bibliotheque
                elif evennements_fenetre.key == K_2 or evennements_fenetre.key == K_KP2:
                    obj_courant = "m"  #mur
                elif evennements_fenetre.key == K_3 or evennements_fenetre.key == K_KP3:
                    obj_courant = "t"  #toit
                elif evennements_fenetre.key == K_4 or evennements_fenetre.key == K_KP4:
                    obj_courant = "d"  #sable
                elif evennements_fenetre.key == K_5 or evennements_fenetre.key == K_KP5:
                    obj_courant = "e"  #eau
                elif evennements_fenetre.key == K_6 or evennements_fenetre.key == K_KP6:
                    obj_courant = "s"  #sol
                elif evennements_fenetre.key == K_7 or evennements_fenetre.key == K_KP7:
                    obj_courant = "h"  #herbe
                elif evennements_fenetre.key == K_8 or evennements_fenetre.key == K_KP8:
                    obj_courant = "a"  #minerai d'or
                elif evennements_fenetre.key == K_9 or evennements_fenetre.key == K_KP9:
                    obj_courant = "0"  #vide
                #controle du tchat
                elif evennements_fenetre.key == K_0 or evennements_fenetre.key == K_KP0:
                    txt_chat = dlb.DialogBox(fenetre, "Que voulez-vous dire ?", "Chat", rcenter, grd_font, y_ecart, type_btn=2, carte=carte).render()
                    time_blitting_txt_chat = time.time() + 10
                    if txt_chat[:16] == 'toggledownfalled':
                        carte.set_meteo('toggledownfalled')
                    elif txt_chat[:6] == 'invert':
                        carte.set_meteo('invert')
                    elif txt_chat[:4] == 'tp->':
                        go_to = txt_chat[4::]
                        go_to = go_to.split(',')
                        x_ = personnage.get_pos()[0] // 30 + carte.get_fov()[0]
                        x_ -= int(go_to[0])
                        new0 = carte.get_fov()[0] - x_ if carte.get_fov()[0] - x_ >= 0 else 0
                        new0 = new0 if new0 <= 4096 - (carte.get_fov()[1] - carte.get_fov()[0]) else 4096 - (carte.get_fov()[1] - carte.get_fov()[0])
                        carte.set_fov(new0, new0 + (carte.get_fov()[1] - carte.get_fov()[0]))
                    if en_reseau:
                        reseau_speaking(socket_client_serv, txt_chat, params_co, personnage, carte, blocs)
                #controle pour courir
                elif evennements_fenetre.key == K_RETURN:
                    #pour courir
                    print(personnage.get_speed())
                    courir_bool = True if not courir_bool else False
                    new_speed = personnage.get_speed() + 50 if courir_bool else personnage.get_speed() - 50
                    personnage.set_speed(new_speed)

        #on affiche le personnage
        personnage.render()

        if vip_bool:
            if int(time.time() * 10) % 3 == 0 and not vu_vip_change:
                index_couleur = (index_couleur + 1) % (len(liste_couleur) - 1)
                pseudo_aff = font.render(pseudo, 1, liste_couleur[index_couleur])
                vu_vip_change = True
            elif int(time.time() * 10) % 3:
                vu_vip_change = False
        fenetre.blit(pseudo_aff, (personnage.get_pos()[0] - len(pseudo), personnage.get_pos()[1] - 12))

        #musique
        if time.time() >= last_music_time and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(random.choice(music_liste))
            pygame.mixer.music.play()
            last_music_time = time.time() + 360

        #affichage du personnage en fonction de la souris
        if xy_s < personnage.get_pos()[0]:  #souris à gauche
            situation_actuelle = 'gauche'
            personnage.change_direction(situation_actuelle, mouse=True)
        else:  #souris à droite
            situation_actuelle = 'droite'
            personnage.change_direction(situation_actuelle, mouse=True)

        if prise_de_degats > 0:
            personnage.encaisser_degats(0.5)
            afficher_degats_pris(fenetre, nombre_degats, font, personnage.get_pos())
            falling.play()
            falling.stop()
            prise_de_degats = 0

        if show_cursor:
            #mouvement permanent de la souris
            xy_s, xy_s1 = souris_ou_t_es(fenetre, arme_h_g)
            #affichage du bloc en cours d'utilisation
            aff_bloc(root, obj_courant, carte.get_img_dict(), rcenter, lst_inventaire, blocs.dict_name(), font, blocs)
        else:
            x_pos, y_pos = pygame.mouse.get_pos()

            #on affiche les caractéristiques du bloc survolé :)
            if carte.get_tile(x_pos // 30 + carte.get_fov()[0], y_pos // 30) != 'p':
                bloc_actuel = carte.get_tile(x_pos // 30 + carte.get_fov()[0], y_pos // 30) if not marteau.has_been_2nd_planed(carte.get_tile(x_pos // 30 + carte.get_fov()[0], y_pos // 30)) else carte.get_tile(x_pos // 30 + carte.get_fov()[0], y_pos // 30)[2::]
                bloc_carac = font.render(blocs.dict_name()[bloc_actuel] + ' : %3i,' % blocs.get(bloc_actuel) + ' x:{}, y:{}'.format(str(x_pos // 30 + carte.get_fov()[0]), str(y_pos // 30)), 1, (10, 10, 10))
                pygame.draw.rect(fenetre, (150, 150, 150), (
                    x_pos, y_pos,
                    4 + bloc_carac.get_size()[0],
                    4 + bloc_carac.get_size()[1]))
                fenetre.blit(bloc_carac, (x_pos + 2, y_pos + 2))

        #saut
        if saut and time_saut <= time.time():
            time_saut = time.time() + temps_saut_attendre
            if personnage.get_pos()[1] + (liste_hauteur_saut[hauteur_saut % len(liste_hauteur_saut)] * 30) >= 0 and \
                    not carte.collide(personnage.get_pos()[0] // 30 + carte.get_fov()[0], personnage.get_pos()[1] // 30 +
                            (liste_hauteur_saut[hauteur_saut % len(liste_hauteur_saut)])):
                personnage.set_y(personnage.get_pos()[1] + (liste_hauteur_saut[hauteur_saut % len(liste_hauteur_saut)]) * 30)
            hauteur_saut += 1
            if hauteur_saut == len(liste_hauteur_saut) - 1:
                saut = False
                hauteur_saut = 0

        #gravité active non bloquante
        if personnage.get_pos()[1] // 30 + 1 <= 18:
            if carte.get_tile(personnage.get_pos()[0] // 30 + carte.get_fov()[0], personnage.get_pos()[1] // 30 + 1) not in blocs.list_solid() \
                    and carte.get_tile(personnage.get_pos()[0] // 30 + carte.get_fov()[0], personnage.get_pos()[1] // 30 + 1) != './' \
                    and not saut:
                personnage.set_y(personnage.get_pos()[1] + 30)
                nb_cases_chut += 1
                if nb_cases_chut >= 3:
                    prise_de_degats = 1
            else:
                nb_cases_chut = 0

        #affichage de l'année
        pygame.draw.rect(root, (150, 150, 150), (8, 9, 78, 19))
        root.blit(font.render('Année :: ' + str(annee + 1), 1, (0, 0, 0)), (14, 10))

        #affichage du 'suiveur'
        pygame.draw.rect(fenetre, (180, 25, 150), (last_pos[0], last_pos[1], 30, 30))

        #affichage du chat
        if txt_chat != "" or time.time() <= time_blitting_txt_chat:
            txt_afficher_chat = font.render(txt_chat, 1, (10, 10, 10))
            pygame.draw.rect(fenetre, (150, 150, 150), (personnage.get_pos()[0] + 30,
                                                        personnage.get_pos()[1] - txt_afficher_chat.get_size()[1] - 10,
                                                        txt_afficher_chat.get_size()[0] + 4,
                                                        txt_afficher_chat.get_size()[1] + 1))
            fenetre.blit(txt_afficher_chat, (personnage.get_pos()[0] + 32, personnage.get_pos()[1] - 7 - txt_afficher_chat.get_size()[1]))

        if en_reseau:
            actualise_chat(socket_client_serv, params_co, fenetre, font)

        if time.time() >= tps_tour:
            tps_tour = time.time() + 0.1
            FPS.timer(cpt_tour)
            cpt_tour = 0

        #items
        marteau.update()

        #fin de boucle
        cpt_tour += 1
        #if not en_reseau:
        #    FPS.pause()

        #affichage des FPS
        fps_stp(temps_avant_fps, root, rcenter, font)
        pygame.display.flip()