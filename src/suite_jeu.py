# -*-coding: utf8-*

import gamecore
import dialog_box as dlb
import os
from commerces_p import message_affiche
import pickle
import socket
import personnage_code
import ded_manager as ded
import niveau as niveau_pkg
import weather
import pygame
import ombrage_bloc as omb


def jeu(hote, port, en_reseau, root, fenetre, creatif, dossier_personnage, rcenter, blocs, hauteur_fen):
    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "dossier.sav", "wb") as dossier_ecrire:
        pickle.Pickler(dossier_ecrire).dump(dossier_personnage)
    
    font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 8)
    grd_font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 12)
    params_co = (hote, port)
    y_ecart = (root.get_size()[1] - 600) // 2

    #variables
    pseudo = ""
    shader = omb.Shader(fenetre, blocs)
    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "pseudo.sav", "r") as pseudo_lire:
        pseudo = pseudo_lire.read()
    #réseau
    if not en_reseau:
        carte = niveau_pkg.Carte(fenetre, root, fenetre.get_size()[0] // 30 + 1, blocs, shader)
        carte.load(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")
        socket_client_serv = None
    else:
        try:
            socket_client_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            params_co = (hote, port)
            socket_client_serv.sendto(pickle.dumps([pseudo, 0, 0, dossier_personnage]), params_co)
            tmp = socket_client_serv.recv(4096)
            if pickle.loads(tmp):
                #on recoit un booleen indiquant si le serveur veut un mot de passe ou non
                #on demande un mot de passe
                mdp_to_send = dlb.DialogBox(fenetre, "Vous devez vous identifier :", "Authentification réseau", rcenter, grd_font, y_ecart, type_btn=2).render()
                socket_client_serv.sendto(pickle.dumps(mdp_to_send), params_co)
                #on a envoyé le mot de passe et on recoit la reponse du serveur :
                #True si on est accepté, False si on l'est pas
                tmp2 = socket_client_serv.recv(4096)
                if not pickle.loads(tmp2):
                    #on est pas accepté, on quitte le mode réseau
                    dlb.DialogBox(fenetre, ["Le mot de passe est faux /", "Vous n'avez pas de compte"], "Erreur", rcenter, grd_font, y_ecart, type_btn=0).render()
                    en_reseau = False
                    message_affiche("Le serveur n'est pas joignable, le jeu quitte le mode réseau.", rcenter)
                    carte = niveau_pkg.Carte(fenetre, root, fenetre.get_size()[0] // 30 + 1, blocs, shader)
                    carte.load(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")
                else:
                    #tout est correct !
                    en_reseau = True
                    carte = niveau_pkg.LANMap(fenetre, root, fenetre.get_size()[0] // 30 + 1, socket_client_serv, params_co, blocs, shader)
                    carte.receive_map()
            else:
                #il n'y avait pas besoin de mot de passe, on se connecte normalement et on demande la map :)
                en_reseau = True
                carte = niveau_pkg.LANMap(fenetre, root, fenetre.get_size()[0] // 30 + 1, socket_client_serv, params_co, blocs, shader)
                carte.receive_map()
        except OSError:
            en_reseau = False
            message_affiche("Le serveur n'est pas joignable, le jeu quitte le mode réseau.", rcenter)
            carte = niveau_pkg.Carte(fenetre, root, fenetre.get_size()[0] // 30 + 1, blocs, shader)
            carte.load(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")

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
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav', 'rb') as f:
            if pickle.Unpickler(f).load():
                carte.add_meteo(vent)
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav', 'rb') as f:
            if pickle.Unpickler(f).load():
                carte.add_meteo(vent)
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav', 'rb') as f:
            if pickle.Unpickler(f).load():
                carte.add_meteo(vent)
    
    dust_electricty_driven_manager = ded.DustElectricityDriven(carte, font, fenetre, en_reseau=en_reseau)

    game = gamecore.Game(fenetre, personnage, en_reseau, blocs, creatif, params_co, root, carte,
                         rcenter, dust_electricty_driven_manager, socket_client_serv, hauteur_fen)
    game.lite_start()
