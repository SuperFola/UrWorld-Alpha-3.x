# -*-coding: utf8-*

import gamecore
import dialog_box as dlb
import os
from commerces_p import message_affiche
import pickle
import socket
import personnage_code
import items as itm
import niveau as niveau_pkg
import weather
import pygame
import ombrage_bloc as omb


def jeu(hote, port, en_reseau, root, fenetre, creatif, dossier_personnage, rcenter):
    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "dossier.sav", "wb") as dossier_ecrire:
        pickle.Pickler(dossier_ecrire).dump(dossier_personnage)
    
    font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 8)
    grd_font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 12)
    marteau = itm.Marteau(rcenter, fenetre, font)
    params_co = (hote, port)
    y_ecart = (root.get_size()[1] - 600) // 2

    #les blocks
    blocs = niveau_pkg.Inventory()
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
    blocs.add('aaa', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Interrupteur on', tps_explode=0, take_fire=False)
    blocs.add('bbb', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Interrupteur off', tps_explode=0, take_fire=False)
    blocs.add('ccc', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Cable', tps_explode=0, take_fire=False)
    blocs.add('ddd', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Lampe on', tps_explode=0, take_fire=False)
    blocs.add('eee', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Lampe off', tps_explode=0, take_fire=False)
    blocs.add('fff', solid=False, shadow=0, gravity=False, quantity=10, innafichable=False, name='Répéteur de courant', tps_explode=0, take_fire=False)
    blocs.add('ggg', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Bloc de commande', tps_explode=0, take_fire=False)
    blocs.add('hhh', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Piston', tps_explode=0, take_fire=False)
    blocs.add('iii', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Piston collant', tps_explode=0, take_fire=False)
    blocs.add('jjj', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Conteneur', tps_explode=0, take_fire=False)
    
    #variables
    pseudo = ""
    shader = omb.Shader(fenetre, blocs)
    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "pseudo.sav", "r") as pseudo_lire:
        pseudo = pseudo_lire.read()
    #réseau
    if not en_reseau:
        carte = niveau_pkg.Carte(fenetre, root, marteau, fenetre.get_size()[0] // 30 + 1, blocs, shader)
        carte.load(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")
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
                    carte = niveau_pkg.Carte(fenetre, root, marteau, fenetre.get_size()[0] // 30 + 1, blocs, shader)
                    carte.load(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl")
                else:
                    #tout est correct !
                    en_reseau = True
                    carte = niveau_pkg.LANMap(fenetre, root, marteau, fenetre.get_size()[0] // 30 + 1, socket_client_serv, params_co, blocs, shader)
                    carte.receive_map()
            else:
                #il n'y avait pas besoin de mot de passe, on se connecte normalement et on demande la map :)
                en_reseau = True
                carte = niveau_pkg.LANMap(fenetre, root, marteau, fenetre.get_size()[0] // 30 + 1, socket_client_serv, params_co, blocs, shader)
                carte.receive_map()
        except OSError:
            en_reseau = False
            message_affiche("Le serveur n'est pas joignable, le jeu quitte le mode réseau.", rcenter)
            carte = niveau_pkg.Carte(fenetre, root, marteau, fenetre.get_size()[0] // 30 + 1, blocs, shader)
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
    
    dust_electricty_driven_manager = itm.DustElectricityDriven(carte, font, fenetre, en_reseau=en_reseau)

    game = gamecore.Game(fenetre, personnage, en_reseau, blocs, creatif, marteau, params_co, root, carte,
                         rcenter, dust_electricty_driven_manager, socket_client_serv)
    game.start()