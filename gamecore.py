import os
import dialog_box as dlb
import constantes as cst
import time
import socket
from niveau import Carte, LANMap
from commerces_p import message_affiche, message_affiche_large, passant_parle
import pygame
import pickle
from pygame.locals import *


class Game:
    def __init__(self, surface, personnage, en_reseau, blocs, creatif, marteau, params_co_network, root_surface):
        self.fenetre = surface
        self.root = root_surface
        self.personnage = personnage
        self.en_reseau = en_reseau
        self.blocs = blocs
        self.equipement_courant = '0'
        self.numero_niv = 'map'
        self.carte = []
        self.teleporteurs = []
        self.creatif = creatif
        self.pancartes_lst = []
        self.inventaire = []
        self.windowed_is = False
        self.marteau = marteau
        self.params_co = params_co_network
        self.nb_blocs_large = self.fenetre.get_size()[0] // 30 + 1
        self.rcenter = self.fenetre.get_size()[0] // 2, self.fenetre.get_size()[1] // 2
        self.last_music_time = time.time() + 30   # Secondes
        self.FPS = cst.IAFPS(75)
        self.cpt_tour = 0
        self.tps_tour = time.time() + 1
        self.nom_mechant = "Gordavus"
        self.volume_son_j = 50

    def load_coponents(self):
        #Pygame elements
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
        # Pickling elements
        with open("Parties" + os.sep + "inventaire.sav", "rb") as inventory_r:
            self.inventaire = pickle.Unpickler(inventory_r).load()
        with open("Parties" + os.sep + "equipement_en_cours.sav", "rb") as lire_equipement:
            self.obj_courant = pickle.Unpickler(lire_equipement).load()
            self.number_of_case = {v: k for k, v in enumerate([elt for line in self.inventaire for elt in line])}[self.obj_courant]
        with open("Parties" + os.sep + "niveau.sav", "rb") as niv_lire:
            self.numero_niv = pickle.Unpickler(niv_lire).load()
        with open("Parties" + os.sep + "bloc.sav", "rb") as bloc_lire:
            self.blocs = pickle.Unpickler(bloc_lire).load()
        with open("Parties" + os.sep + "pos.sav", "rb") as pos_lire:
            self.personnage.set_pos(pickle.Unpickler(pos_lire).load())
        with open("Parties" + os.sep + "fov.sav", "rb") as fov_lire:
            new = pickle.Unpickler(fov_lire).load()
            self.carte.set_fov(new[0], new[1])
        with open("Parties" + os.sep + "mana.sav", "rb") as mana_lire:
            self.personnage.set_mana(pickle.Unpickler(mana_lire).load())
        with open("Parties" + os.sep + "couleur.sav", "r") as couleur_lire:
            self.carte.set_background_color(eval(couleur_lire.read()))
        with open("Parties" + os.sep + "teleporteurs.sav", "rb") as teleport_lire:
            self.teleporteurs = pickle.Unpickler(teleport_lire).load()
        with open("Parties" + os.sep + "gamemode.sav", "rb") as creatifmode_lire:
            self.creatif = pickle.Unpickler(creatifmode_lire).load()
        with open("Parties" + os.sep + "shader.sav", "rb") as shader_lire:
            self.carte.set_current_shader(pickle.Unpickler(shader_lire).load())
        with open("Parties" + os.sep + "pancartes.sav", "rb") as lire_pancartes:
            self.pancartes_lst = pickle.Unpickler(lire_pancartes).load()
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
        # Variables
        if not self.en_reseau:
            self.carte = Carte(self.fenetre, self.root, self.marteau, self.nb_blocs_large, self.blocs)
            self.carte.load("Niveaux" + os.sep + "map.lvl")
        else:
            try:
                socket_client_serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                socket_client_serv.sendto(pickle.dumps([self.personnage.get_pseudo(), 0, 0, self.personnage.get_dossier()]), self.params_co)
                self.carte = []
                self.carte = LANMap(self.fenetre, self.root, self.marteau, self.nb_blocs_large, socket_client_serv, self.params_co, self.blocs)
                self.carte.receive_map()
            except OSError:
                self.en_reseau = False
                message_affiche("Le serveur n'est pas joignable, le jeu quitte le mode réseau.", self.rcenter)
                self.carte = Carte(self.fenetre, self.root, self.marteau, self.nb_blocs_large, self.blocs)
                self.carte.load("Niveaux" + os.sep + "map.lvl")
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
            self.socket_client_serv.sendto(pickle.dumps("get->configuration"), self.params_co)
            data_serv = []
            with open("Parties" + os.sep + "serveur.sav", "rb+") as data_serv_wrb:
                data_serv = pickle.Unpickler(data_serv_wrb).load()
                temp = self.socket_client_serv.recv(4096)
                temp = pickle.loads(temp)
                for i in range(len(data_serv)):
                    if data_serv[i][0] == str(self.params_co[0]) + ':' + str(self.params_co[1]):
                        data_serv[i][1] = temp[0]
                        data_serv[i][2] = temp[1]
                        break
                pickle.Pickler(data_serv_wrb).dump(data_serv)
            with open("Parties" + os.sep + "serveur.sav", "wb") as f:
                pickle.Pickler(f).dump(data_serv)

    def save(self):
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
        s = [elt for line in self.inventaire for elt in line]
        if direction == 'bas':
            self.number_of_case = self.number_of_case + 1 if self.number_of_case + 1 <= len(s) - 1 else len(s) - 1
        elif direction == 'haut':
            self.number_of_case = self.number_of_case - 1 if self.number_of_case - 1 >= 0 else 0
        self.obj_courant = s[self.number_of_case]

    def get_events(self):
        for ev in [pygame.event.poll()]:
            if ev.type == KEYDOWN and (ev.key == K_ESCAPE or ev.key == K_F4):
                self.save()
                self.continuer = 0
            elif ev.type == QUIT and self.windowed_is:
                self.save()
            #controles au clavier
            elif ev.type == KEYDOWN:
                #controles de déplacement au clavier
                if ev.key == K_UP:
                    #on monte
                    self.personnage.move("haut")
                elif ev.key == K_DOWN:
                    #on descend mais uniquement si il y a une echelle en dessous de nous
                    if self.carte.get_tile(self.personnage.get_pos()[0] // 30 + self.carte.get_fov()[0],self. personnage.get_pos()[1] // 30 + 1) == './':
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

    def start(self):
        self.load_coponents()
        self.continuer = 1
        while self.continuer:
            self.get_events()
            #blit ici
            pygame.display.flip()
        self.save()