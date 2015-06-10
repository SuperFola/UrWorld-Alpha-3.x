# -*-coding: utf8-*

import os
from random import choice as randchoice
from glob import glob
from math import trunc
import dialog_box as dlb
import constantes as cst
import time
import socket
from niveau import Carte, LANMap, img_
from commerces_p import message_affiche, message_affiche_large, passant_parle, message_affiche_non_bloquant
import pygame
import pickle
from pygame.locals import *


testeur = os.path.exists("test.test")


def padding_0(liste):
    intermediaire = []
    for i in liste:
        temp = str(int(i[21::].split('.')[0]))
        intermediaire.append('0' * (4 - len(temp)) + str(temp))
    intermediaire.sort()
    return intermediaire


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


class Game:
    def __init__(self, surface, personnage, en_reseau, blocs, creatif, marteau, params_co_network, root_surface, carte, rcenter):
        """
        :param surface: a pygame sub-surface
        :param personnage: an instance of the class Personnage
        :param en_reseau: a boolean who say if you are connect to a network or not
        :param blocs: an instance of the class Blocks
        :param creatif: a boolean who say if you are in infinite creation mode or not
        :param marteau: an instance of the class Marteau
        :param params_co_network: the parameters to connect the socket to the network
        :param root_surface: a pygame surface (the window)
        :return: nothing
        """
        self.fenetre = surface
        self.root = root_surface
        self.personnage = personnage
        self.en_reseau = en_reseau
        self.network = None
        self.blocs = blocs
        self.equipement_courant = '0'
        self.numero_niv = 'map'
        self.carte = carte
        self.teleporteurs = []
        self.creatif = creatif
        self.pancartes_lst = []
        self.inventaire = []
        self.windowed_is = False
        self.marteau = marteau
        self.params_co = params_co_network
        self.nb_blocs_large = self.fenetre.get_size()[0] // 30 + 1
        self.rcenter = self.fenetre.get_size()[0] // 2, rcenter[1]  # self.fenetre.get_size()[1] // 2
        self.last_music_time = time.time() + 30   # Secondes
        self.FPS = cst.IAFPS(75)
        self.cpt_tour = 0
        self.tps_tour = time.time() + 1
        self.nom_mechant = "Gordavus"
        self.volume_son_j = 50
        self.font = pygame.font.Font("freesansbold.otf", 8)
        self.font2 = pygame.font.Font("freesansbold.otf", 10)
        self.grd_font = pygame.font.Font("freesansbold.otf", 12)
        self.y_ecart = (self.root.get_size()[1] - 600) // 2
        self.max_scrolling = 4096
        self.obj_courant = '0'
        self.petits_blocs = img_
        self.index_couleur = 0
        self.last_vie = 100
        self.liste_couleur = [
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
        self.temps_saut_attendre = 0.125
        self.liste_hauteur_saut = [
            -1,
            -1,
            -1,
            +1,
            +1,
            +1,
            +1,
        ]
        self.hauteur_saut = 0
        self.show_cursor = False
        self.annee = len(glob("Niveaux" + os.sep + "Olds Maps" + os.sep + "*.lvl")) + 1
        self.music_liste = [
            "Sons" + os.sep + "urworld1.wav",
            "Sons" + os.sep + "urworld2.wav"
        ]
        self.number_of_case = 0
        self.boumList = []
        self.breakListe = []
        self.liste_septre = [
            'D', 'F',
            'G', 'H',
            'J', 'K'
        ]
        self.jump_height = 3
        self.dico_cd = cst.cds
        self.show_stats = True
        self.saut = False
        self.nb_cases_chut = 0
        self.clique_gauche = 0
        self.vu_vip_change = False
        self.var_gravite = 0.142
        self.courir_bool = False
        self.last_cd_used = ""
        self.indice_son = 0
        self.prise_de_degats = 0
        self.vip_bool = os.path.exists("Personnage" + os.sep + "0" + os.sep + "vip.file")
        if self.vip_bool:
            tmp = open("Personnage" + os.sep + "0" + os.sep + "vip.file", "r")
            if tmp.read() != self.personnage.get_pseudo() + "::VIP":
                self.vip_bool = False
            tmp.close()

    def load_coponents(self):
        """
        load all the files, the surfaces, the sound ... that the game need to work
        :return: nothing
        """
        #Pygame elements
        #surfaces
        self.check = pygame.image.load("Particules" + os.sep + "check_vert.png").convert_alpha()
        self.arme_h_g = pygame.image.load("Personnage" + os.sep + "A" + os.sep + "sword_up_g.png").convert_alpha()

        #activation de la répétition des touches
        pygame.key.set_repeat(200, self.personnage.get_speed())

        #on n'affiche pas le curseur de la souris !
        pygame.mouse.set_visible(False)

        #si on est en créatif, on a tout les blocs en *9999 !
        if not self.creatif or self.vip_bool:
            #on est encore et quand même en créatif :D
            for index in self.blocs.list():
                if self.blocs.get(index) < 900 and index not in ('bn', 'n?', '?.', '/§', '§%'):
                    quant = 5000 if not self.creatif else self.blocs.get(index) + 150
                    self.blocs.set(index, nbr=quant)

        # Musics
        self.falling = pygame.mixer.Sound("Sons" + os.sep + "falling.wav")
        self.explode = pygame.mixer.Sound("Sons" + os.sep + "explode.wav")
        self.eau_bruit = pygame.mixer.Sound("Sons" + os.sep + "water.wav")
        self.breaking_bloc = pygame.mixer.Sound("Sons" + os.sep + "wooden.wav")
        self.volume = pygame.mixer.music.get_volume()  # Retourne la valeur du volume, entre 0 et 1
        pygame.mixer.music.set_volume(self.volume_son_j / 4 * 3)  # Réglage du volume

        # Pickling elements
        if os.path.exists("Parties" + os.sep + "inventaire.sav"):
            with open("Parties" + os.sep + "inventaire.sav", "rb") as inventory_r:
                self.inventaire = pickle.Unpickler(inventory_r).load()
        if os.path.exists("Parties" + os.sep + "equipement_en_cours.sav"):
            with open("Parties" + os.sep + "equipement_en_cours.sav", "rb") as lire_equipement:
                self.obj_courant = pickle.Unpickler(lire_equipement).load()
                self.number_of_case = {v: k for k, v in enumerate([elt for line in self.inventaire for elt in line])}[self.obj_courant]
        else:
            self.obj_courant = self.inventaire[0][0]
            self.number_of_case = 0
        if os.path.exists("Parties" + os.sep + "niveau.sav"):
            with open("Parties" + os.sep + "niveau.sav", "rb") as niv_lire:
                self.numero_niv = pickle.Unpickler(niv_lire).load()
        else:
            self.numero_niv = "map"
        if os.path.exists("Parties" + os.sep + "bloc.sav"):
            with open("Parties" + os.sep + "bloc.sav", "rb") as bloc_lire:
                self.blocs = pickle.Unpickler(bloc_lire).load()
        if os.path.exists("Parties" + os.sep + "pos.sav"):
            with open("Parties" + os.sep + "pos.sav", "rb") as pos_lire:
                self.personnage.set_pos(pickle.Unpickler(pos_lire).load())
        else:
            self.personnage.set_pos((0, 0))
        if os.path.exists("Parties" + os.sep + "fov.sav"):
            with open("Parties" + os.sep + "fov.sav", "rb") as fov_lire:
                new = pickle.Unpickler(fov_lire).load()
                self.carte.set_fov(new[0], new[1])
        else:
            self.carte.set_fov(0, self.fenetre.get_size()[0] // 30 + 1)
        if os.path.exists("Parties" + os.sep + "mana.sav"):
            with open("Parties" + os.sep + "mana.sav", "rb") as mana_lire:
                self.personnage.set_mana(pickle.Unpickler(mana_lire).load())
        else:
            self.personnage.set_mana(100)
        if os.path.exists("Parties" + os.sep + "couleur.sav"):
            with open("Parties" + os.sep + "couleur.sav", "r") as couleur_lire:
                self.carte.set_background_color(eval(couleur_lire.read()))
        else:
            self.carte.set_background_color((20, 180, 20))
        if os.path.exists("Parties" + os.sep + "teleporteurs.sav"):
            with open("Parties" + os.sep + "teleporteurs.sav", "rb") as teleport_lire:
                self.teleporteurs = pickle.Unpickler(teleport_lire).load()
        else:
            self.teleporteurs = []
        if os.path.exists("Parties" + os.sep + "gamemode.sav"):
            with open("Parties" + os.sep + "gamemode.sav", "rb") as creatifmode_lire:
                self.creatif = pickle.Unpickler(creatifmode_lire).load()
        else:
            self.creatif = True
        if os.path.exists("Parties" + os.sep + "shader.sav"):
            with open("Parties" + os.sep + "shader.sav", "rb") as shader_lire:
                self.carte.set_current_shader(pickle.Unpickler(shader_lire).load())
        else:
            self.carte.set_current_shader("nul")
        if os.path.exists("Parties" + os.sep + "pancartes.sav"):
            with open("Parties" + os.sep + "pancartes.sav", "rb") as lire_pancartes:
                self.pancartes_lst = pickle.Unpickler(lire_pancartes).load()
        else:
            self.pancartes_lst = []

        # Files
        with open("Parties" + os.sep + "pseudo.sav", "r") as nom_perso:  #pour le pseudo
            self.personnage.set_pseudo(nom_perso.read())
        with open("bonjour.txt", "r") as msg_bjr_lire:
            self.grd_msg_bjr = str(msg_bjr_lire.read()).format(self.personnage.get_pseudo(), self.nom_mechant)
            self.grd_msg_bjr += "\n" * 4 + "Bonne aventure `{0}` !".format(self.personnage.get_pseudo())
        if os.path.exists("Personnage" + os.sep + "0" + os.sep + "vip.file"):
            with open("Personnage" + os.sep + "0" + os.sep + "vip.file", "r") as lire_vip:
                if lire_vip.read() == self.personnage.get_pseudo() + "::VIP":
                    self.vip_bool = True
                else:
                    self.vip_bool = False

        # Chargement obligatoire
        self.carte.load_image()

        # Chargements optionnels
        if os.path.exists('Parties' + os.sep + 'texture_pack.sav'):
            with open('Parties' + os.sep + 'texture_pack.sav', 'r') as txtpr:
                self.carte.set_texture_pack(txtpr.read())
        if os.path.exists('Parties' + os.sep + 'jheight.sav'):
            with open('Parties' + os.sep + 'jheight.sav', 'r') as jhr:
                self.jump_height = int(jhr.read())
            liste_hauteur_saut = [-1 for _ in range(self.jump_height + 1)] + [+1 for _ in range(self.jump_height + 2)]
        if os.path.exists('Parties' + os.sep + 'jtime.sav'):
            with open('Parties' + os.sep + 'jtime.sav', 'r') as tjr:
                self.temps_saut_attendre = int(tjr.read()) / 1000
        if not os.path.exists('Parties' + os.sep + 'pos.sav'):
            #création de nouveau fichiers
            message_affiche_large(self.grd_msg_bjr, self.fenetre, self.rcenter)

        # Personnal elements
        if self.en_reseau:
            self.network.sendto(pickle.dumps("get->configuration"), self.params_co)
            data_serv = []
            with open("Parties" + os.sep + "serveur.sav", "rb+") as data_serv_wrb:
                data_serv = pickle.Unpickler(data_serv_wrb).load()
                temp = self.network.recv(4096)
                temp = pickle.loads(temp)
                for i in range(len(data_serv)):
                    if data_serv[i][0] == str(self.params_co[0]) + ':' + str(self.params_co[1]):
                        data_serv[i][1] = temp[0]
                        data_serv[i][2] = temp[1]
                        break
                pickle.Pickler(data_serv_wrb).dump(data_serv)
            with open("Parties" + os.sep + "serveur.sav", "wb") as f:
                pickle.Pickler(f).dump(data_serv)

        # A lancer apres avoir chargé || initialisé une Carte | LANMap
        self.img_tous_blocs = self.carte.get_img_dict()

    def actualise_chat(self):
        """
        a function who ask to have the messages of the chat, and who draw it
        :return: nothing
        """
        self.network.sendto(pickle.dumps("get->chat"), self.params_co)
        temp = self.network.recv(4096)
        temp = pickle.loads(temp)
        surf = pygame.Surface((420, 22 * 6))
        surf.fill(0x000000)
        surf.set_alpha(60)
        surf.convert_alpha()
        self.fenetre.blit(surf, (self.fenetre.get_size()[0] - 430, self.fenetre.get_size()[1] - surf.get_size()[1] - 10))
        for i in range(len(temp)):
            msg = temp[i][0]
            color = temp[i][1]
            rendu = self.font.render(msg, 1, color)
            self.fenetre.blit(rendu, (self.fenetre.get_size()[0] - 420, i * rendu.get_size()[1] + (self.fenetre.get_size()[1] - surf.get_size()[1] - 10)))

    def boum_atomique(self, x, y):
        """
        a function who destroy a bomb and some blocs aroud it
        :param x: position of the bomb
        :param y: second position of the bomb
        :return: nothing
        """
        explode_list = [
            (x-3, y),
            (x-2, y),
            (x-1, y),
            (x+1, y),
            (x+2, y),
            (x+3, y),
            (x-1, y-1),
            (x-2, y-1),
            (x, y-1),
            (x+1, y-1),
            (x+2, y-1),
            (x, y-2),
            (x-1, y-2),
            (x+1, y-2),
            (x, y+1),
            (x-1, y+1),
            (x-2, y+1),
            (x-3, y+1),
            (x+1, y+1),
            (x+2, y+1),
            (x+3, y+1),
            (x, y+2),
            (x-1, y+2),
            (x+1, y+2)
        ]
        for i in explode_list:
            if 0 <= i[0] <= self.max_scrolling and 0 <= i[1] <= self.carte.get_y_len():
                if self.carte.get_tile(i[0], i[1]) != 'cv':
                    self.carte.remove_bloc(i[0], i[1], '0')
                elif self.carte.get_tile(i[0], i[1]) == 'cv' and i != (x, y):
                    self.boumList.append([time.time(), (i[0], i[1])])
                elif self.carte.get_tile(i[0], i[1]) == 'cv' and i[0] == x and i[1] == y:
                    self.carte.remove_bloc(x, y, '0')

    def save(self):
        """
        a function to save some dependencies of the game
        :return: nothing
        """
        print("\n\n" + "*" * 34 + " SAUVEGARDE " + "*" * 34 + "\n")
        self.carte.save()
        #avec Pickle
        with open("Parties" + os.sep + "inventaire.sav", "wb") as inventory_w:
            pickle.Pickler(inventory_w).dump(self.inventaire)
        with open("Parties" + os.sep + "equipement_en_cours.sav", "wb") as ecrire_equipement:
            pickle.Pickler(ecrire_equipement).dump(self.equipement_courant)
        with open("Parties" + os.sep + "niveau.sav", "wb") as niv_ecrire:
            pickle.Pickler(niv_ecrire).dump(self.numero_niv)
        with open("Parties" + os.sep + "bloc.sav", "wb") as bloc_save:
            pickle.Pickler(bloc_save).dump(self.blocs)
        with open("Parties" + os.sep + "pos.sav", "wb") as pos_save:
            pickle.Pickler(pos_save).dump(self.personnage.get_pos())
        with open("Parties" + os.sep + "fov.sav", "wb") as fov_ecrire:
            pickle.Pickler(fov_ecrire).dump(self.carte.get_fov())
        with open("Parties" + os.sep + "mana.sav", "wb") as mana_ecrire:
            pickle.Pickler(mana_ecrire).dump(self.personnage.get_mana())
        with open("Parties" + os.sep + "couleur.sav", "w") as couleur_ecrire:
            couleur_ecrire.write(str(self.carte.get_background_color()))
        with open("Parties" + os.sep + "teleporteurs.sav", "wb") as teleport_ecrire:
            pickle.Pickler(teleport_ecrire).dump(self.teleporteurs)
        with open("Parties" + os.sep + "gamemode.sav", "wb") as creatifmode_ecrire:
            pickle.Pickler(creatifmode_ecrire).dump(self.creatif)
        with open("Parties" + os.sep + "shader.sav", "wb") as shader_ecrire:
            pickle.Pickler(shader_ecrire).dump(self.carte.get_curent_shader())
        with open("Parties" + os.sep + "pancartes.sav", "wb") as ecrire_pancartes:
            pickle.Pickler(ecrire_pancartes).dump(self.pancartes_lst)
        print('Sauvegarde réussie !\n\n')

    def molette_(self, direction):
        """
        a function who change the current bloc you are using
        :param direction: the direction of the mouse wheel
        :return: nothing
        """
        s = [elt for line in self.inventaire for elt in line]
        if direction == 'bas':
            self.number_of_case = self.number_of_case + 1 if self.number_of_case + 1 <= len(s) - 1 else len(s) - 1
        elif direction == 'haut':
            self.number_of_case = self.number_of_case - 1 if self.number_of_case - 1 >= 0 else 0
        self.obj_courant = s[self.number_of_case]

    def print_fps(self):
        """
        a function to calculate the FPS and draw it on the screen
        :return: nothing
        """
        vrais_fps = trunc(((1000 / (time.time() - self.temps_avant_fps)) / 1000) if time.time() - self.temps_avant_fps else 300)
        titre = "/* FPS : %5i */" % vrais_fps
        pygame.draw.rect(self.root, (75, 155, 180), (0, self.rcenter[1] + 360, 115, 20))
        self.root.blit(self.font.render(titre, 1, (10, 10, 10)), (4, self.rcenter[1] + 362))

    def s_invent_dd(self, bloc_choisi, tout, obj_survol):
        """
        a function to to draw the inventory elements
        :param bloc_choisi: the current bloc
        :param tout: if we want to see all the specifications of the blocs or not
        :param obj_survol: the bloc your mouse if on
        :return: nothing
        """
        vide_choisi = False
        for y_, ligne in enumerate(self.inventaire):
            for x_, x_s in enumerate(ligne):
                nom_entite = x_s
                if self.marteau.has_been_2nd_planed(x_s):
                    x_s = x_s[2::]
                if x_s in self.blocs.list():
                    self.fenetre.blit(self.img_tous_blocs[x_s], (x_ * 31 + 52, y_ * 31 + 52))
                    if x_s == bloc_choisi and bloc_choisi != '0':
                        self.fenetre.blit(self.check, (x_ * 31 + 52, y_ * 31 + 52))
                    elif x_s == '0' and bloc_choisi == '0' and not vide_choisi:
                        self.fenetre.blit(self.check, (x_ * 31 + 52, y_ * 31 + 52))
                        vide_choisi = True
                if tout:
                    if self.marteau.has_been_2nd_planed(nom_entite):
                        nom_entite = nom_entite[2::]
                    if nom_entite != "0" and nom_entite in self.blocs.list() and self.blocs.get(nom_entite) <= 999:
                        #sinon on aura des gros trait blancs tout moches :P
                        nb = self.font.render("%3i" % self.blocs.get(nom_entite), 1, (240, 240, 240))
                        self.fenetre.blit(nb, (52 + x_ * 31, 52 + y_ * 31))
                    elif self.blocs.get(nom_entite) > 999 and nom_entite != "0" and nom_entite in self.blocs.list():
                        nb = self.font.render("N/A", 1, (240, 240, 240))
                        self.fenetre.blit(nb, (52 + x_ * 31, 52 + y_ * 31))
                else:
                    breaking = False
                    entite = self.inventaire[y_][x_]
                    if entite == obj_survol and not breaking:
                        if self.blocs.get(entite) <= 999:
                            nb = self.font.render(self.blocs.dict_name()[entite] + " : %3i" % self.blocs.get(entite), 1, (240, 240, 240))
                            pygame.draw.rect(self.fenetre, (150, 150, 150), (50 + x_ * 31 + 30, 50 + y_ * 31 + 30, nb.get_size()[0] + 2, nb.get_size()[1] + 2))
                            self.fenetre.blit(nb, (52 + x_ * 31 + 30, 52 + y_ * 31 + 30))
                            breaking = True
                        elif self.blocs.get(entite) > 999:
                            nb = self.font.render(self.blocs.dict_name()[entite] + " : N/A", 1, (240, 240, 240))
                            pygame.draw.rect(self.fenetre, (150, 150, 150), (50 + x_ * 31 + 30, 50 + y_ * 31 + 30, nb.get_size()[0] + 2, nb.get_size()[1] + 2))
                            self.fenetre.blit(nb, (52 + x_ * 31 + 30, 52 + y_ * 31 + 30))
                            breaking = True

    def afficher_degats_pris(self):
        """
        a function who draw the damage you had took
        :return: nothing
        """
        x = self.personnage.get_pos()[0] - 2
        y = self.personnage.get_pos()[1] - 30
        self.fenetre.blit(self.font.render("-" + str(0.5), 1, (208, 6, 6)), (x, y))

    def drag_and_drop_invent(self):
        """
        a function who draw and managed the events you create when the inventory is open
        :return: nothing
        """
        continue3, clic = 1, 0
        obj_pris, obj_avant = "", ""
        obj_retour_actu = self.obj_courant
        obj_survol = ""
        last_x, last_y = 0, 0
        #affichage du curseur de la souris
        pygame.mouse.set_visible(True)

        tout = False

        structure_niveau = self.carte.get_list()

        liste_innafichable_dad = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'c', '/§', '§%', 'Q', 'S']

        #carte affichage type bandeau / reader-like
        numero_niv = self.carte.get_fov()[0]
        decalage_x = 0
        slice_ = [0, 54]
        structure = structure_niveau
        center_screen = (600 - 250) // 2
        center_x = self.rcenter[0] - 580 // 2 + 740 // 2 - 10
        inventaire = pygame.image.load("Fond" + os.sep + "inventaire.png").convert_alpha()
        carte_img = pygame.image.load("Fond" + os.sep + "carte.png").convert_alpha()

        while continue3:
            self.carte.render()

            #on dessine le fond (et accessoirement on efface ainsi la fenetre) :
            self.fenetre.blit(inventaire, (10, 10))

            #carte
            self.fenetre.blit(carte_img, (center_x - 16, center_screen - 8))
            self.fenetre.blit(self.font2.render("*-* Carte *-*", 1, (220, 220, 220)), (center_x + 580 // 2 - 40, center_screen))
            carte_miniature = [line[slice_[0]:slice_[1]] for line in structure]
            for y_ in range(20):
                for x_ in range(len(carte_miniature[0])):
                    case = carte_miniature[y_][x_]
                    case = case if not self.marteau.has_been_2nd_planed(case) else case[2::]
                    if case not in liste_innafichable_dad:
                        self.fenetre.blit(self.petits_blocs[case], ((x_ * 10) + center_x + 10,
                                                            (y_ * 10) + center_screen + 30))
                    elif case == '0':
                        pygame.draw.rect(self.fenetre, (30, 150, 205), (x_ * 10 + center_x + 10,
                                                                   y_ * 10 + center_screen + 30,
                                                                   10, 10))
                    else:
                        pygame.draw.rect(self.fenetre, (250, 150, 205), (x_ * 10 + center_x + 10,
                                                                   y_ * 10 + center_screen + 30,
                                                                   10, 10))

            #et on met les icones et leur quantité !
            self.s_invent_dd(obj_retour_actu, tout, obj_survol)

            #et enfin on laisse TOUT LE TEMPS le bloc suivre la souris, si y en a un ;)
            x_souris, y_souris = self.souris_ou_t_es()

            if obj_pris != "":
                #y a un bloc qui doit suivre la souris !
                self.fenetre.blit(self.img_tous_blocs[obj_pris], (x_souris, y_souris))

            #gestion des events
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_pris = self.inventaire[yi][xi]
                            last_x, last_y = xi, yi
                            self.inventaire[yi][xi] = "0"  #on vide la case !
                        clic = 1  #clic actif
                    elif event.button == 3:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_retour_actu = self.inventaire[yi][xi]
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8 \
                                and obj_pris != "":
                            obj_avant = self.inventaire[yi][xi]
                            self.inventaire[last_y][last_x] = obj_avant
                            self.inventaire[yi][xi] = obj_pris
                            obj_retour_actu = obj_pris
                            obj_pris = ""
                            clic = 0  #clic non actif
                        else:
                            self.inventaire[last_y][last_x] = obj_pris
                            obj_pris = ""
                            clic = 0  #clic non actif
                    elif event.button == 3:
                        xi = (event.pos[0] - 52) // 31
                        yi = (event.pos[1] - 52) // 31
                        if event.pos[0] >= 52 and event.pos[0] <= 52 + 31 * 16 and event.pos[1] >= 52 and event.pos[1] <= 52 + 31 * 8:
                            obj_retour_actu = self.inventaire[yi][xi]
                elif event.type == MOUSEMOTION:
                    xi = event.pos[0]
                    yi = event.pos[1]
                    if clic and obj_pris != "":
                        #déplacement car clic est ok, bouton gauche enfoncé (ou droit)
                        #faut que le bloc suive la souris !
                        self.fenetre.blit(self.img_tous_blocs[obj_pris], (xi, yi))
                    else:
                        if xi >= 52 and xi <= 52 + 31 * 16 and yi >= 52 and yi <= 52 + 31 * 8:
                            yi_selec = (yi - 52) // 31
                            xi_selc = (xi - 52) // 31
                            if 0 <= yi_selec <= len(self.inventaire) - 1 and 0 <= xi_selc <= len(self.inventaire[0]) - 1:
                                obj_survol = self.inventaire[yi_selec][xi_selc]
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

            message_affiche_non_bloquant("Vous êtes actuellement dans la section : " + str(numero_niv) + "/" + str(self.max_scrolling) + ".", self.rcenter)
            pygame.display.flip()

        if obj_retour_actu != "":
            self.obj_courant = obj_retour_actu
        self.number_of_case = {v: k for k, v in enumerate([elt for line in self.inventaire for elt in line])}[self.obj_courant]

    def souris_ou_t_es(self):
        """
        a function who calculate the position of the mouse and draw the cursor
        :return: nothing
        """
        x_souris, y_souris = pygame.mouse.get_pos()
        self.fenetre.blit(self.arme_h_g, (x_souris, y_souris))
        pygame.mouse.set_visible(False)
        return x_souris, y_souris

    def aff_bloc(self):
        """
        a function who draw your unclickable hotbar and the blocs who are near of the current bloc you are using
        :return: nothing
        """
        liste_ordre_invent = []
        pos_bloc = 0
        for ligne in self.inventaire:
            for element in ligne:
                liste_ordre_invent.append(element)
        for x, case in enumerate(liste_ordre_invent):
            if case == self.obj_courant:
                pos_bloc = x
        liste_ordre_invent = liste_ordre_invent[pos_bloc:pos_bloc+9]
        centrage = self.rcenter[0] - (9 * (34 + 2)) // 2
        for nombre, bloc in enumerate(liste_ordre_invent):
            if bloc != self.obj_courant:
                pygame.draw.rect(self.root, (140, 140, 140), (centrage + nombre * 36, self.rcenter[1] + 310, 34, 34))
            elif bloc == self.obj_courant:
                pygame.draw.rect(self.root, (0, 0, 0), (centrage + nombre * 36, self.rcenter[1] + 310 + 30 + 4, 300, 30))
                self.root.blit(self.font.render(self.blocs.get_name(bloc) + " : " + str(self.blocs.get(bloc)), 1,
                                      (255, 255, 255), (0, 0, 0)),
                                      (centrage + nombre * 36, self.rcenter[1] + 310 + 30 + 4))
                pygame.draw.rect(self.root, (41, 235, 20), (centrage + nombre * 36, self.rcenter[1] + 310, 34, 34))
            self.root.blit(self.img_tous_blocs[bloc], (centrage + nombre * 36 + 2, self.rcenter[1] + 310 + 2))

    def flash(self):
        """
        a function who flash your screen
        :return: nothing
        """
        pygame.draw.rect(self.fenetre, (240, 240, 240), (0, 0, self.fenetre.get_size()[0], 600))
        pygame.display.flip()
        pygame.time.wait(0.1)
        self.carte.render()
        pygame.display.flip()

    def time_cruise(self):
        """
        a function who draw the GUI, and manage it, who allow you to go on an older map
        :return: nothing
        """
        vieille_carte = None
        field_of_view_chose = 0
        width_ = 500
        height_ = 450
        continuer = 1
        liste_cartes = [i for i in glob("Niveaux" + os.sep + "Olds Maps" + os.sep + "*.lvl")]
        liste_cartes_originelles = liste_cartes
        liste_cartes = padding_0(liste_cartes)
        choisi = -1

        while continuer:
            self.carte.render()
            pygame.draw.rect(self.fenetre, (80, 160, 80), ((self.fenetre.get_size()[0] - width_) // 2,
                                                  300 - (height_ // 2),
                                                  width_,
                                                  height_))
            for i in range(len(liste_cartes)):
                if 300 - (height_ // 2) <= 310 - (height_ // 2) + i * 32 + field_of_view_chose <= height_ + 268 - (height_ // 2):
                    if choisi == i:
                        pygame.draw.rect(self.fenetre, (85, 215, 45), ((self.fenetre.get_size()[0] - width_) // 2 + 10,
                                                            310 - (height_ // 2) + i * 32 + field_of_view_chose,
                                                            width_ - 10 * 2, 30))
                    else:
                        pygame.draw.rect(self.fenetre, (45, 175, 190), ((self.fenetre.get_size()[0] - width_) // 2 + 10,
                                                            310 - (height_ // 2) + i * 32 + field_of_view_chose,
                                                            width_ - 10 * 2, 30))
            for i, j in enumerate(liste_cartes):
                nom_destination = ('Année ' + j).replace(' 0', ' ').replace(' 0', ' ').replace(' 0', ' ')
                if 300 - (height_ // 2) <= 310 - (height_ // 2) + i * 32 + field_of_view_chose <= height_ + 268 - (height_ // 2):
                    self.fenetre.blit(self.font.render(nom_destination, 1, (10, 10, 10)),
                                 ((self.fenetre.get_size()[0] - width_) // 2 + 10,
                                 310 - (height_ // 2) + i * 32 + field_of_view_chose))

            pygame.draw.rect(self.fenetre, (85, 215, 45), ((self.fenetre.get_size()[0] - width_) // 2 + 10,
                                                      310 + height_ // 2 - 40,
                                                      35, 20))

            x_s, x_s1 = self.souris_ou_t_es()

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
                        if (self.fenetre.get_size()[0] - width_) // 2 + 10 <= x_s <= (self.fenetre.get_size()[0] - width_) // 2 + 10 + 35 \
                                and 310 + height_ // 2 - 40 <= x_s1 <= 310 + height_ // 2 - 20:
                            continuer = 0
                        elif (self.fenetre.get_size()[0] - width_) // 2 <= x_s <= (self.fenetre.get_size()[0] - width_) // 2 + width_:
                            choisi = (x_s1 - (310 - (height_ // 2) + field_of_view_chose)) // 32
            pygame.display.flip()

        if choisi != -1 and 0 <= choisi <= len(liste_cartes) - 1:
            self.carte.load(liste_cartes_originelles[choisi])
            self.flash()

        self.personnage.set_y(0)

        self.annee = choisi if choisi != -1 else self.annee

    def mettre_eau(self, x_blit, y_blit):
        """
        a function who put the water tile on the map
        :param x_blit: the position of the mouse click
        :param y_blit: the second position of the mouse click
        :return:
        """
        y_bloque = []
        cpt_blit_eau = 0
        for i in range(y_blit, 20):
            if self.carte.get_tile(x_blit, i) == "0":
                if i not in y_bloque:
                    self.carte.remove_bloc(x_blit, i, '0')
            else:
                y_bloque.append(i)
            cpt_blit_eau += 1
            for j in range(x_blit - cpt_blit_eau, x_blit + cpt_blit_eau):
                if j >= 0 and j <= self.carte.get_x_len():
                    #pour ne pas dépasser
                    if self.carte.get_tile(j, i) == "0" and i not in y_bloque:
                        self.carte.remove_bloc(j, i, 'e')
        self.eau_bruit.play()
        self.eau_bruit.stop()

    def custom(self):
        """
        a function who draw the border of the game
        :return: nothing
        """
        #modification du "launcher"
        pygame.draw.rect(self.root, (0, 0, 0), (self.rcenter[0] - 20, 9, 200, 17))
        #textes
        self.root.blit(self.font.render("Créatif (Off - On)", 1, (255, 255, 255)), (self.rcenter[0] - 10, 12))
        #boutons
        pygame.draw.rect(self.root, (140, 140, 140), (self.rcenter[0] + 120, 9, 43, 17))
        if self.creatif:
            pygame.draw.rect(self.root, (140, 140, 140), (self.rcenter[0] + 120, 10, 43, 15))
            pygame.draw.rect(self.root, (180, 20, 20), (self.rcenter[0] + 120 + 1, 10, 20, 15))
        elif not self.creatif:
            pygame.draw.rect(self.root, (140, 140, 140), (self.rcenter[0] + 120, 10, 43, 15))
            pygame.draw.rect(self.root, (20, 180, 20), (self.rcenter[0] + 120 + 22, 10, 20, 15))
        #actualisation de l'écran pour afficher les changements
        pygame.display.flip()

    def put_blocs(self, x_blit, y_blit):
        """
        a function who do all the test and check if we can put a bloc or not
        :param x_blit: the position of the mouse click
        :param y_blit: the second position of the mouse click
        :return: nothing
        """
        if self.carte.get_tile(x_blit, y_blit) not in self.blocs.list_unprintable():
            if not self.creatif:
                #on est quand meme en créatif x)
                self.carte.remove_bloc(x_blit, y_blit, self.obj_courant)
            if self.creatif:
                #"temps" de destruction d'un bloc
                if self.marteau.has_been_2nd_planed(self.carte.get_tile(x_blit, y_blit)):
                    #item: #0 : x #1 : y #2 : nouveau bloc #3 : temps #4 : heure de la pose
                    self.breakListe.append([x_blit, y_blit, self.obj_courant, self.blocs.get_time(self.carte.get_tile(x_blit, y_blit)[2::]) // 100, time.time()])
                else:
                    #le bloc n'est pas un bloc de second plan
                    #item: #0 : x #1 : y #2 : nouveau bloc #3 : temps #4 : heure de la pose
                    self.breakListe.append([x_blit, y_blit, self.obj_courant, self.blocs.get_time(self.carte.get_tile(x_blit, y_blit)[2::]) // 100, time.time()])
            if self.carte.get_tile(x_blit, y_blit) in list(self.blocs.list()) and self.creatif: #si on est pas en creatif
                #le bloc existe, on met 1 bloc en plus dans l'inventaire
                if self.marteau.has_been_2nd_planed(self.carte.get_tile(x_blit, y_blit)):
                    self.blocs.set(self.carte.get_tile(x_blit, y_blit)[2::], nbr=self.blocs.get(self.carte.get_tile(x_blit, y_blit)[2::])+1)
                else:
                    self.blocs.set(self.carte.get_tile(x_blit, y_blit), nbr=self.blocs.get(self.carte.get_tile(x_blit, y_blit))+1)
            elif self.carte.get_tile(x_blit, y_blit) in self.blocs.list() and self.creatif:
                #le bloc n'existe pas dans l'inventaire, on l'ajoute donc
                self.blocs.add(self.carte.get_tile(x_blit, y_blit), solid=True, shadow=0, gravity=False, quantity=1, innafichable=False, name='No name', tps_explode=0, take_fire=False)
            #on enlève 1 pour le bloc POSé:
            if self.blocs.get(self.obj_courant) - 1 >= 0 and self.creatif:
                self.blocs.use(self.obj_courant)
            if self.obj_courant == 'vb':
                #téléporteur
                if not self.en_reseau:
                    self.teleporteurs.append([len(self.teleporteurs), (x_blit, y_blit)])
                else:
                    self.network.sendto(pickle.dumps('set->telep' + str(x_blit) + ',' + str(y_blit)), self.params_co)
            if self.obj_courant == '%a':
                #pancartes
                if not self.en_reseau:
                    self.pancartes_lst.append([(x_blit, y_blit), ''])
                else:
                    self.network.sendto(pickle.dumps("set->pan" + str(x_blit) + "," + str(y_blit)), self.params_co)
            if self.carte.get_tile(x_blit, y_blit) == '%a' and self.obj_courant != '%a':
                #on casse une pancarte
                if not self.en_reseau:
                    #on doit donc liberer la place pour ne pas perdre en espace disque
                    for i in range(len(self.pancartes_lst)):
                        if self.pancartes_lst[i][0] == (x_blit, y_blit):
                            self.pancartes_lst.pop(i)
                            break
                else:
                    self.network.sendto(pickle.dumps("break->pan" + str(x_blit) + "," + str(y_blit)), self.params_co)
            if self.carte.get_tile(x_blit, y_blit) == 'vb' and self.obj_courant != 'vb':
                #on casse un téléporteur
                if not self.en_reseau:
                    for i in range(len(self.teleporteurs)):
                        if self.teleporteurs[i][1] == (x_blit, y_blit):
                            if self.teleporteurs[i][0] % 2:
                                #impair
                                self.carte.remove_bloc(self.teleporteurs[i][1][0], self.teleporteurs[i][1][1], '0')
                                self.carte.remove_bloc(self.teleporteurs[i - 1][1][0], self.teleporteurs[i - 1][1][1], '0')
                                self.teleporteurs.pop(i)
                                self.teleporteurs.pop(i - 1)
                            elif not self.teleporteurs[i][0] % 2:
                                #pair
                                if not len(self.teleporteurs) % 2:
                                    #la longueur est paire, alors un autre téléporteur est associé a celui ci
                                    #et on doit donc aussi le casser
                                    self.carte.remove_bloc(self.teleporteurs[i + 1][1][0], self.teleporteurs[i + 1][1][1], '0')
                                    self.carte.remove_bloc(self.teleporteurs[i][1][0], self.teleporteurs[i][1][1], '0')
                                    self.teleporteurs.pop(i + 1)
                                    self.teleporteurs.pop(i)
            if self.obj_courant == 'e':
                #eau
                self.carte.remove_bloc(x_blit, y_blit, "e")
                if self.carte.get_tile(x_blit, y_blit) == "e":
                    self.mettre_eau(x_blit, y_blit)

    def get_events(self):
        """
        a function who get the pygame events and run the associate action
        :return: nothing
        """
        for ev in [pygame.event.poll()]:
            if ev.type == KEYDOWN and (ev.key == K_ESCAPE or ev.key == K_F4):
                self.save()
                self.continuer = 0
            elif ev.type == QUIT and self.windowed_is:
                self.save()
            #controles a la souris
            elif ev.type == MOUSEBUTTONDOWN:
                if ev.button == 5:
                    #la molette descend
                    self.molette_('bas')
                elif ev.button == 4:  #la molette monte
                    self.molette_('haut')
                elif ev.button == 1:
                    clique_gauche = 1
                    #clic, donc on pose un bloc là où on a cliqué !
                    x_blit = ev.pos[0] // 30 + self.carte.get_fov()[0]
                    y_blit = ev.pos[1] // 30
                    if y_blit <= 19 and x_blit <= self.max_scrolling - 1 and (self.blocs.get(self.obj_courant) > 0 or not self.creatif) \
                            and ((x_blit, y_blit) != (self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0], self.personnage.get_pos()[1] // 30) or self.obj_courant not in self.blocs.list_solid()) \
                            and self.obj_courant not in self.blocs.list_unprintable():
                        self.put_blocs(x_blit, y_blit)
                elif ev.button == 3 and (self.obj_courant not in self.blocs.list_unprintable() or self.obj_courant == '§%' \
                                                 or self.obj_courant in self.dico_cd.keys()):
                    x_clic = ev.pos[0] // 30 + self.carte.get_fov()[0]
                    y_clic = ev.pos[1] // 30
                    if self.carte.get_tile(x_clic, y_clic) == 'cv':
                        #bombe atomique
                        self.boumList.append([time.time(), (x_clic, y_clic)])
                    elif self.carte.get_tile(x_clic, y_clic) == 'vb':
                        #on veut se téléporter
                        if not self.en_reseau:
                            for i in range(len(self.teleporteurs)):
                                if self.teleporteurs[i][1] == (x_clic, y_clic):
                                    if self.teleporteurs[i][0] % 2:
                                        #impair
                                        #passage en cases
                                        z = self.teleporteurs[i - 1][1][0] - (self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0])
                                        if self.carte.get_fov()[0] + z <= self.max_scrolling - self.carte.get_space():
                                            self.carte.set_fov(self.carte.get_fov()[0] + z, self.carte.get_fov()[1] + z)
                                        else:
                                            self.carte.set_fov(self.max_scrolling - self.carte.get_space(), self.max_scrolling)
                                        self.personnage.set_y((self.teleporteurs[i - 1][1][1] - 1 if y_clic - 1 >= 0 else self.teleporteurs[i - 1][1][1] + 1) * 30)
                                        #pour etre au dessus et pas dedans
                                    elif not self.teleporteurs[i][0] % 2:
                                        #pair
                                        if not len(self.teleporteurs) % 2:
                                            #passage en cases
                                            z = self.teleporteurs[i + 1][1][0] - (self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0])
                                            if self.carte.get_fov()[0] + z <= self.max_scrolling - self.carte.get_space():
                                                self.carte.set_fov(self.carte.get_fov()[0] + z, self.carte.get_fov()[1] + z)
                                            else:
                                                self.carte.set_fov(self.max_scrolling - self.carte.get_space(), self.max_scrolling)
                                            self.personnage.set_y((self.teleporteurs[i + 1][1][1] - 1 if y_clic - 1 >= 0 else self.teleporteurs[i + 1][1][1] + 1) * 30)
                                        elif len(self.teleporteurs) % 2 and i == len(self.teleporteurs) - 1:
                                            message_affiche("Aucune cible n'a été définie pour ce téléporteur !", self.rcenter)
                        else:
                            self.network.sendto(pickle.dumps('get->telep' + str(x_clic) + ',' + str(y_clic)), self.params_co)
                            temp = self.network.recv(4096)
                            temp = pickle.loads(temp)
                            #passage en cases
                            z = temp[0] - (self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0])
                            if self.carte.get_fov()[0] + z <= self.max_scrolling - self.carte.get_space():
                                self.carte.set_fov(self.carte.get_fov()[0] + z, self.carte.get_fov()[1] + z)
                            else:
                                self.carte.set_fov(self.max_scrolling - self.carte.get_space(), self.max_scrolling)
                            self.personnage.set_y((temp[1] - 1 if y_clic - 1 >= 0 else temp[1] + 1) * 30)
                            #pour etre au dessus et pas dedans
                    elif self.obj_courant in self.dico_cd.keys() and self.carte.get_tile(x_clic, y_clic) == 'B':
                        #jukebox
                        self.indice_son = 0 if self.obj_courant == 'qs' else 1
                        self.indice_son = 1 if self.obj_courant == 'sd' else 2
                        self.indice_son = 2 if self.obj_courant == 'df' else 3
                        if not pygame.mixer.music.get_busy():
                            last_cd_used = self.obj_courant
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                            self.blocs.set(self.last_cd_used, nbr=self.blocs.get(self.last_cd_used)+1)
                        pygame.mixer.music.load(self.music_liste[self.indice_son])
                        pygame.mixer.music.play()
                    elif self.obj_courant == '§%' and self.carte.get_tile(x_clic, y_clic) != '0':
                        self.marteau.utiliser(self.carte, y_clic, x_clic)
                    elif self.carte.get_tile(x_clic, y_clic) == '%a':
                        if not self.en_reseau:
                            for i in self.pancartes_lst:
                                if i[0] == (x_clic, y_clic):
                                    if i[1] != '':
                                        message_affiche(i[1], self.rcenter)
                                    else:
                                        i[1] = dlb.DialogBox(self.fenetre, 'Entrez votre texte :', 'Edition d\'une pancarte',
                                                             self.rcenter, self.grd_font, self.y_ecart, type_btn=2, mouse=True,
                                                             carte=self.carte).render()
                                    break
                        else:
                            self.network.sendto(pickle.dumps("get->pan" + str(x_clic) + "," + str(y_clic)), self.params_co)
                            temp = self.network.recv(4096)
                            temp = pickle.loads(temp)
                            if not temp:
                                texte_pan_to_send = dlb.DialogBox(self.fenetre, 'Entrez votre texte :', 'Edition d\'une pancarte',
                                                                  self.rcenter, self.grd_font, self.y_ecart, type_btn=2,
                                                                  mouse=True, carte=self.carte).render()
                                self.network.sendto(pickle.dumps("set->pan" + str(x_clic) + "," + str(y_clic) + "," + texte_pan_to_send), self.params_co)
                            else:
                                message_affiche(temp, self.rcenter)
                    elif self.carte.get_tile(x_clic, y_clic) == '%b':
                        if not self.en_reseau:
                            self.annee = self.time_cruise()
                        else:
                            message_affiche("Vous ne pouvez pas voyager dans le temps en mode réseau", self.rcenter)
            elif ev.type == MOUSEBUTTONUP:
                if ev.button == 1:
                    #clic gauche, on relache la souris donc on met à false le 'booleen' qui dit que l'on peut
                    self.clique_gauche = 0
                elif ev.button == 3:
                    #clique droit
                    if self.obj_courant in self.blocs.list_unprintable():
                        #on enlève 1 potion
                        if self.obj_courant not in self.liste_septre and self.obj_courant not in self.dico_cd.keys() and self.obj_courant not in '§%':
                            self.blocs.use(self.obj_courant)
                        if self.obj_courant == 'Q':
                            self.personnage.update_vie(100)
                        elif self.obj_courant == 'S':
                            self.personnage.update_mana(100)
                        elif self.obj_courant in self.liste_septre:
                            self.personnage.mana_action(self.creatif, self.obj_courant, ev.pos)
                elif ev.button == 2:  #bouton du milieu (molette de la souris)
                    #on a récupéré le bloc et on l'a affecté comme bloc en cours d'utilisation
                    self.obj_courant = self.carte.get_tile((ev.pos[0] // 30) + self.carte.get_fov()[0], (ev.pos[1] // 30))
            elif ev.type == MOUSEMOTION:
                if self.clique_gauche and not self.creatif:
                    #en fait on est en créatif quand meme dans ce cas ci :)
                    x_blit = ev.pos[0] // 30 + self.carte.get_fov()[0]
                    y_blit = ev.pos[1] // 30
                    if y_blit <= 19 and x_blit <= self.max_scrolling and self.blocs.get(self.obj_courant) > 0 \
                            and ((x_blit, y_blit) != (
                                            self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0],
                                            self.personnage.get_pos()[1] // 30) or self.obj_courant not in self.blocs.list_solid()):
                        if self.carte.get_tile(x_blit, y_blit) not in self.blocs.list_unprintable():
                            if self.carte.get_tile(x_blit, y_blit) in self.blocs.list() and self.creatif:
                                #donc si on est en créatif, on ajoute pas
                                #le bloc existe, on met 1 bloc en plus dans l'inventaire
                                #mais on vérifie avant qu'il n'est pas en arriere plan, sans quoi
                                #l'affichage dans l'inventaire ne fonctionnera pas !
                                if self.marteau.has_been_2nd_planed(self.carte.get_tile(x_blit, y_blit)):
                                    self.blocs.set(self.carte.get_tile(x_blit, y_blit)[2::], nbr=self.blocs.get(self.carte.get_tile(x_blit, y_blit)[2::])+1)
                                else:
                                    self.blocs.set(self.carte.get_tile(x_blit, y_blit), nbr=self.blocs.get(self.carte.get_tile(x_blit, y_blit))+1)
                            elif self.creatif and self.carte.get_tile(x_blit, y_blit) not in self.blocs.list():
                                #le bloc n'existe pas dans l'inventaire, on l'ajoute donc
                                self.blocs.add(self.carte.get_tile(x_blit, y_blit), solid=True, shadow=0, gravity=False, quantity=1, innafichable=False, name='No name', tps_explode=0, take_fire=False)
                            #on enlève 1 pour le bloc POSé:
                            if self.blocs.get(self.obj_courant) - 1 >= 0 and self.creatif:
                                self.blocs.use(self.obj_courant)
                            self.carte.remove_bloc(x_blit, y_blit, self.obj_courant)
                            #raffraichir la map pour voir le placement multiple :
                            self.carte.render()
                            if self.show_stats:
                                self.personnage.afficher_vie()
                                self.personnage.afficher_mana()
                                self.marteau.render()
                            if self.obj_courant == 'e':
                                self.mettre_eau(x_blit, y_blit)
            #controles au clavier
            elif ev.type == KEYDOWN:
                #controles de déplacement au clavier
                if ev.key == K_UP:
                    #on monte
                    self.personnage.move("haut")
                elif ev.key == K_DOWN:
                    #on descend mais uniquement si il y a une echelle en dessous de nous
                    if self.carte.get_tile(self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0],
                                           self. personnage.get_pos()[1] // 30 + 1) == './':
                        self.personnage.set_y(self.personnage.get_pos()[1] + 30)
                elif ev.key == K_LEFT:
                    #on va à gauche
                    self.personnage.move("gauche")
                    self.personnage.change_direction("gauche")
                elif ev.key == K_RIGHT:
                    #on va à droite
                    self.personnage.move("droite")
                    self.personnage.change_direction("droite")
                #changement de la taille du FOV
                elif ev.key == K_e:
                    new_size_fov = dlb.DialogBox(self.fenetre, ["Entrez la nouvelle taille du", "FOV (entre 0 et " + str(self.nb_blocs_large) + " ) :"],
                                  "Réglage du FOV", self.rcenter, self.grd_font, self.y_ecart, type_btn=3, carte=self.carte).render()
                    if new_size_fov.isdigit():
                        self.carte.set_fov(self.carte.get_fov()[0], self.carte.get_fov()[0] + abs(int(new_size_fov)))
                #controles discuter et inventaire
                elif ev.key == K_d:
                    #on parle à la personne la plus proche de soi
                    passant_parle(self.fenetre, self.personnage.get_direction(), self.personnage, self.carte.get_list(),
                                  self.blocs.get('/§'), self.rcenter, self.carte.get_img_dict(), self.carte.get_fov())
                elif ev.key == K_i:
                    #la musique en pause ou pas !
                    if pygame.music.get_busy():
                        pygame.mixer.music.set_volume(0)
                    elif not pygame.music.get_busy():
                        pygame.mixer.music.set_volume(self.volume_son_j)
                #on affiche les autres ou pas :D
                elif ev.key == K_p:
                    if self.en_reseau:
                        self.carte.change_oth_visibility()
                        dlb.DialogBox(self.fenetre, "Les autres joueurs ne sont plus visibles" if not self.carte.get_oth_visibility() else "Les autres joueurs sont visibles",
                                    "Visiblité des joueurs", self.rcenter, self.grd_font, self.y_ecart, type_btn=0, carte=self.carte).render()
                elif ev.key == K_y:
                    self.carte.switch_shader()
                elif ev.key == K_t:
                    self.show_cursor = not self.show_cursor
                #saut
                elif ev.key == K_SPACE:
                    self.saut = True
                    self.time_saut = time.time() + self.temps_saut_attendre
                #controle pour courir
                elif ev.key == K_RETURN:
                    #pour courir
                    self.courir_bool = not self.courir_bool
                    new_speed = self.personnage.get_speed() + 50 if self.courir_bool else self.personnage.get_speed() - 50
                    self.personnage.set_speed(new_speed)
                #controle de l'affichage de l'inventaire Drag&Drop
                elif ev.key == K_LSHIFT or ev.key == K_RSHIFT:
                    self.drag_and_drop_invent()
                #controle du tchat
                elif ev.key == K_0 or ev.key == K_KP0:
                    txt_chat = dlb.DialogBox(self.fenetre, "Que voulez-vous dire ?", "Chat", self.rcenter, self.grd_font, self.y_ecart, type_btn=2, carte=self.carte).render()
                    time_blitting_txt_chat = time.time() + 10
                    if txt_chat[:16] == 'toggledownfalled':
                        self.carte.set_meteo('toggledownfalled')
                    elif txt_chat[:6] == 'invert':
                        self.carte.set_meteo('invert')
                    elif txt_chat[:4] == 'tp->':
                        go_to = txt_chat[4::].split(',')
                        x_ = self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0] - int(go_to[0])
                        new0 = self.carte.get_fov()[0] - x_ if self.carte.get_fov()[0] - x_ >= 0 else 0
                        new0 = new0 if new0 <= 4096 - (self.carte.get_fov()[1] - self.carte.get_fov()[0]) else 4096 - (self.carte.get_fov()[1] - self.carte.get_fov()[0])
                        self.carte.set_fov(new0, new0 + (self.carte.get_fov()[1] - self.carte.get_fov()[0]))
                    if self.en_reseau:
                        self.reseau_speaking(self.network, txt_chat, self.params_co, self.personnage, self.carte, self.blocs)
                elif ev.key == K_o:
                    if self.creatif:
                        self.creatif = False
                        pygame.draw.rect(self.root, (140, 140, 140), (self.rcenter[0] + 120, 9, 43, 17))
                        pygame.draw.rect(self.root, (20, 180, 20), (self.rcenter[0] + 120 + 1, 10, 20, 15))
                        self.personnage.set_vie(self.last_vie)
                    elif not self.creatif:
                        self.creatif = True
                        pygame.draw.rect(self.root, (140, 140, 140), (self.rcenter[0] + 120, 9, 43, 17))
                        pygame.draw.rect(self.root, (180, 20, 20), (self.rcenter[0] + 120 + 22, 10, 20, 15))
                        self.last_vie = self.personnage.get_vie()
                        self.personnage.set_vie(100)
                #passage fullscreen -> windowed / windowed -> fullscreen
                elif ev.key == K_u:
                    if self.windowed_is:
                        self.root = pygame.display.set_mode((0, 0), FULLSCREEN)
                        r = pygame.Rect(0, 0, self.fenetre.get_size()[0], 600)  #definition de la taille de la fenetre de jeu
                        r.center = self.root.get_rect().center  #centrage de la fenetre par rapport a l'ecran total
                        self.fenetre = self.root.subsurface(r)  #definition de la fenetre de jeu
                        pygame.display.update(r)  #mise a jour de la fenetre seulement
                        self.custom()
                        self.windowed_is = False
                    else:
                        self.root = pygame.display.set_mode((0, 0))
                        r = pygame.Rect(0, 0, self.fenetre.get_size()[0], 600)  #definition de la taille de la fenetre de jeu
                        r.center = self.root.get_rect().center  #centrage de la fenetre par rapport a l'ecran total
                        self.fenetre = self.root.subsurface(r)  #definition de la fenetre de jeu
                        pygame.display.update(r)  #mise a jour de la fenetre seulement
                        self.custom()
                        pygame.display.set_caption("UrWorld")
                        self.windowed_is = True

    def start(self):
        """
        the main function of this class. run the main thread and load the different coponents
        :return: nothing
        """
        self.continuer = 1
        self.tps_tour = time.time() + 0.1
        self.temps_avant_fps = time.time()
        self.load_coponents()

        x_souris, y_souris = 0, 0
        txt_chat = ""
        time_blitting_txt_chat = 0
        nb_cases_chut = 0
        pseudo_aff = self.font.render(self.personnage.get_pseudo(), 1, (0, 0, 0))

        #le "tour" de l'ecran de jeu
        self.custom()

        while self.continuer:
            #pour les FPS
            self.temps_avant_fps = time.time()

            if not self.en_reseau:
                self.carte.update()
            else:
                self.carte.update_([self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0],
                                     self.personnage.get_pos()[1] // 30, self.personnage.get_direction()])
            #destruction des bombes atomiques non bloquantes
            iBList = 0
            while iBList <= len(self.boumList) - 1:
                item = self.boumList[iBList]
                if time.time() - item[0] > 2:
                    self.boum_atomique(item[1][0], item[1][1])
                    self.boumList.pop(iBList)
                iBList += 1
            #destruction des blocs non bloquant
            iBreakList = 0
            while iBreakList <= len(self.breakListe) - 1:
                item = self.breakListe[iBreakList]
                if time.time() - item[4] > item[3]:
                    self.carte.remove_bloc(item[0], item[1], item[2])
                    self.breakListe.pop(iBreakList)
                    self.breaking_bloc.play()
                iBreakList += 1

            #vie & mana
            if self.show_stats:
                self.personnage.afficher_vie()
                self.personnage.afficher_mana()
                self.marteau.render()
            #régénration de la mana
            self.personnage.regen_mana()

            #pour la souris
            x_souris, y_souris = self.souris_ou_t_es()

            #pour le suiveur
            last_pos = (self.personnage.get_pos()[0] - 30, self.personnage.get_pos()[1]) if self.personnage.get_direction() == 'droite' else (self.personnage.get_pos()[0] + 30, self.personnage.get_pos()[1])

            #pour les events
            self.get_events()

            #gestion du réseau ici
            if self.en_reseau:
                self.actualise_chat()
                if time.time() >= self.tps_tour:
                    tps_tour = time.time() + 0.1
                    self.FPS.timer(self.cpt_tour)
                    self.cpt_tour = 0

            #items
            self.marteau.update()

            #fin de boucle => régulation et affichage des FPS
            self.cpt_tour += 1
            if not self.en_reseau:
                self.FPS.pause()
            self.print_fps()

            #blit ici de toutes les surfaces
            #on affiche le personnage
            self.personnage.render()

            if self.vip_bool:
                if int(time.time() * 10) % 3 == 0 and not self.vu_vip_change:
                    self.index_couleur = (self.index_couleur + 1) % (len(self.liste_couleur) - 1)
                    pseudo_aff = self.font.render(self.personnage.get_pseudo(), 1, self.liste_couleur[self.index_couleur])
                    self.vu_vip_change = True
                elif int(time.time() * 10) % 3:
                    self.vu_vip_change = False
            self.fenetre.blit(pseudo_aff, (self.personnage.get_pos()[0] - len(self.personnage.get_pseudo()), self.personnage.get_pos()[1] - 12))

            #musique
            if time.time() >= self.last_music_time and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(randchoice(self.music_liste))
                pygame.mixer.music.play()
                self.last_music_time = time.time() + 360

            #affichage du personnage en fonction de la souris
            if x_souris < self.personnage.get_pos()[0]:
                #souris à gauche
                self.personnage.change_direction('gauche', mouse=True)
            else:
                #souris à droite
                self.personnage.change_direction('droite', mouse=True)

            if self.prise_de_degats > 0:
                self.personnage.encaisser_degats(0.5)
                self.afficher_degats_pris()
                self.falling.play()
                self.falling.stop()
                self.prise_de_degats = 0

            self.aff_bloc()

            if self.show_cursor:
                #on affiche les caractéristiques du bloc survolé :)
                if self.carte.get_tile(x_souris // 30 + self.carte.get_fov()[0], y_souris // 30) != 'p':
                    bloc_actuel = self.carte.get_tile(x_souris // 30 + self.carte.get_fov()[0], y_souris // 30) if not self.marteau.has_been_2nd_planed(self.carte.get_tile(x_souris // 30 + self.carte.get_fov()[0], y_souris // 30)) else self.carte.get_tile(x_souris // 30 + self.carte.get_fov()[0], y_souris // 30)[2::]
                    bloc_carac = self.font.render(self.blocs.dict_name()[bloc_actuel] + ' : %3i,' % self.blocs.get(bloc_actuel) + ' x:{}, y:{}'.format(str(x_souris // 30 + self.carte.get_fov()[0]), str(y_souris // 30)), 1, (10, 10, 10))
                    pygame.draw.rect(self.fenetre, (150, 150, 150), (
                        x_souris, y_souris,
                        4 + bloc_carac.get_size()[0],
                        4 + bloc_carac.get_size()[1]))
                    self.fenetre.blit(bloc_carac, (x_souris + 2, y_souris + 2))

            #saut
            if self.saut and self.time_saut <= time.time():
                self.time_saut = time.time() + self.temps_saut_attendre
                if self.personnage.get_pos()[1] + (self.liste_hauteur_saut[self.hauteur_saut % len(self.liste_hauteur_saut)] * 30) >= 0 and \
                        not self.carte.collide(self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0], self.personnage.get_pos()[1] // 30 +
                                (self.liste_hauteur_saut[self.hauteur_saut % len(self.liste_hauteur_saut)])):
                    self.personnage.set_y(self.personnage.get_pos()[1] + (self.liste_hauteur_saut[self.hauteur_saut % len(self.liste_hauteur_saut)]) * 30)
                self.hauteur_saut += 1
                if self.hauteur_saut == len(self.liste_hauteur_saut) - 1:
                    self.saut = False
                    self.hauteur_saut = 0

            #gravité active non bloquante
            if self.personnage.get_pos()[1] // 30 + 1 <= 18:
                if self.carte.get_tile(self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0], self.personnage.get_pos()[1] // 30 + 1) not in self.blocs.list_solid() \
                        and self.carte.get_tile(self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0], self.personnage.get_pos()[1] // 30 + 1) != './' \
                        and not self.saut:
                    self.personnage.set_y(self.personnage.get_pos()[1] + 30)
                    self.nb_cases_chut += 1
                    if self.nb_cases_chut >= 3:
                        self.prise_de_degats = 1
                else:
                    self.nb_cases_chut = 0

            #affichage de l'année
            pygame.draw.rect(self.root, (150, 150, 150), (8, 9, 78, 19))
            self.root.blit(self.font.render('Année :: ' + str(self.annee + 1), 1, (0, 0, 0)), (14, 10))

            #affichage du 'suiveur'
            pygame.draw.rect(self.fenetre, (180, 25, 150), (last_pos[0], last_pos[1], 30, 30))

            #affichage du chat
            if txt_chat != "" or time.time() <= time_blitting_txt_chat:
                txt_afficher_chat = self.font.render(txt_chat, 1, (10, 10, 10))
                pygame.draw.rect(self.fenetre, (150, 150, 150), (self.personnage.get_pos()[0] + 30,
                                                            self.personnage.get_pos()[1] - txt_afficher_chat.get_size()[1] - 10,
                                                            txt_afficher_chat.get_size()[0] + 4,
                                                            txt_afficher_chat.get_size()[1] + 1))
                self.fenetre.blit(txt_afficher_chat, (self.personnage.get_pos()[0] + 32, self.personnage.get_pos()[1] - 7 - txt_afficher_chat.get_size()[1]))

            pygame.display.flip()
        self.save()