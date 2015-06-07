import constantes as cst
import os
import pygame
from pygame.locals import *
import pickle
from commerces_p import message_affiche_large
import time

taille_sprite = cst.taille_sprite

#initialisation de font
pygame.font.init()

#police
font = pygame.font.Font("freesansbold.otf", 8)


class Vie:
    def __init__(self, ecran, center):
        self.vie = 100
        self.ecran = ecran
        self.center = center
        self.mort_bruit = pygame.mixer.Sound("Sons" + os.sep + "died.wav")
        self.msg_mort = ""
        with open("message_mort.txt", "r") as lire_mort:
            self.msg_mort = lire_mort.read()
        self.img_vie = pygame.image.load("Particules" + os.sep + "imgo2.png").convert_alpha()

    def update(self, to_add):
        self.vie += to_add
        if self.vie > 100:
            self.vie = 100

    def encaisser_degats(self, degats):
        self.vie -= degats
        if self.vie < 0:
            self.mourrir()

    def render(self):
        #la vie maximum est = à 50 pt_vie
        #fonction qui gérera la vie avec des rect et changera la couleur et tout et tout
        couleur = (50, 180, 0)
        if self.vie >= 40:
            couleur = (50, 180, 0)
        elif 30 <= self.vie <= 39:
            couleur = (80, 150, 0)
        elif 20 <= self.vie <= 29:
            couleur = (120, 110, 0)
        elif 10 <= self.vie <= 19:
            couleur = (160, 70, 0)
        elif 0 < self.vie <= 9:
            couleur = (210, 30, 0)
        if self.vie > 0:
            pygame.draw.rect(self.ecran, couleur, (1105, 7, int(self.vie * 2.5), 14))
            self.ecran.blit(self.img_vie, (1102, 5))
            self.ecran.blit(font.render("Vie : %3i" % self.vie, 1, (10, 10, 10)), (1296, 6))

    def mourrir(self):
        self.mort_bruit.play()
        message_affiche_large(self.msg_mort, self.ecran, self.center)
        self.vie = 100

    def set(self, new):
        self.vie = new

    def get(self):
        return self.vie


class LANVie(Vie):
    def __init__(self, ecran, center, socket_serveur, addr):
        super().__init__(ecran, center)
        self.sock = socket_serveur
        self.addr = addr

    def render(self):
        #fonction qui gérera la vie avec des rect et changera la couleur et tout et tout
        self.get()
        couleur = (50, 180, 0)
        if self.vie >= 40:
            couleur = (50, 180, 0)
        elif 30 <= self.vie <= 39:
            couleur = (80, 150, 0)
        elif 20 <= self.vie <= 29:
            couleur = (120, 110, 0)
        elif 10 <= self.vie <= 19:
            couleur = (160, 70, 0)
        elif 0 < self.vie <= 9:
            couleur = (210, 30, 0)
        if self.vie > 0:
            pygame.draw.rect(self.ecran, couleur, (1105, 7, int(self.vie * 2.5), 14))
            self.ecran.blit(self.img_vie, (1102, 5))
            self.ecran.blit(font.render("Vie : %3i" % self.vie, 1, (10, 10, 10)), (1296, 6))

    def get(self):
        self.sock.sendto(pickle.dumps('get->life'), self.addr)
        self.vie = pickle.loads(self.sock.recv(4096))
        return self.vie

    def set(self, new):
        self.sock.sendto(pickle.dumps('get->life'), self.addr)
        work = pickle.loads(self.sock.recv(4096))
        intermede = new - work
        self.sock.sendto(pickle.dumps('set->life' + str(intermede)), self.addr)
        self.get()

    def update(self, to_add):
        self.sock.sendto(pickle.dumps('set->life' + str(to_add)), self.addr)
        self.get()

    def encaisser_degats(self, degats):
        self.sock.sendto(pickle.dumps('set->life' + str(-degats)), self.addr)
        if self.get() == 0:
            self.mourrir()
        self.set(100)


class Mana:
    def __init__(self, ecran, carte, blocs):
        self.mana = 100
        self.ecran = ecran
        self.img_mana = pygame.image.load("Particules" + os.sep + "imgo.png").convert_alpha()
        self.carte = carte
        self.blocs = blocs
        self.v_droite = 1
        self.v_gauche = -1
        self.liste_mana_action = {
            'laser': 12,
            'teleporte': 8,
            'feu': 4,
            'conic': 6,
            'sphere': 8,
            'build': 12
        }
        self.dico_img = {
            'laser': [pygame.image.load("Particules" + os.sep + "laser.png").convert_alpha(), 12],
            'feu': 4,
            'build': 12,
            'sphere': [pygame.image.load("Particules" + os.sep + "boule.png").convert_alpha(), 8],
            'conic': [pygame.image.load("Particules" + os.sep + "conic.png").convert_alpha(), 6]
        }

    def update(self):
        self.mana += 0.025
        if self.mana > 100:
            self.mana = 100

    def add(self, quantity):
        self.mana += quantity
        if self.mana > 100:
            self.mana = 100

    def render(self):
        #la mana maximum est = à 50 pt_mana
        #fonction qui gérera la mana avec des rect et changera la couleur et tout et tout
        couleur = (17, 58, 160)
        if self.mana >= 40:
            couleur = (17, 58, 160)
        elif 30 <= self.mana <= 39:
            couleur = (20, 62, 175)
        elif 20 <= self.mana <= 29:
            couleur = (22, 70, 192)
        elif 10 <= self.mana <= 19:
            couleur = (25, 77, 215)
        elif 0 < self.mana <= 9:
            couleur = (30, 85, 230)
        if self.mana >= 0:
            pygame.draw.rect(self.ecran, couleur, (7, 7, int(self.mana * 2.5), 14))
            self.ecran.blit(self.img_mana, (5, 5))
            self.ecran.blit(font.render("Mana : %3i" % self.mana, 1, (10, 10, 10)), (185, 6))

    def set(self, new):
        self.mana = new

    def get(self):
        return self.mana

    def action(self, action, creatif, obj_courant, pos, pos_player):
        direction = self.v_droite if pos[0] > pos_player[0] else self.v_gauche
        if self.mana - self.liste_mana_action[action] >= 0 or not creatif:
            #vérification que l'on peut utiliser la mana
            if obj_courant == 'D':
                action = 'laser'
            if obj_courant == 'F':
                action = 'teleporte'
            if obj_courant == 'G':
                action = 'feu'
            if obj_courant == 'H':
                action = 'conic'
            if obj_courant == 'J':
                action = 'sphere'
            if obj_courant == 'K':
                action = 'build'
            #on determine les actions a effectuer ici
            if action == 'teleporte':
                #on se téléporte au lieu du clique
                if self.carte.get_tile((pos[0] // 30 + self.carte.get_fov()[0]), (pos[1] // 30)) not in self.blocs.list_unprintable():
                    #on ne se téléporte pas si il y a le bloc indestructible
                    return (pos[0] // 30) * 30, (pos[1] // 30) * 30

                if creatif:
                    #on est pas en créatif
                    #on enlève des pt de mana
                    self.add(-self.liste_mana_action[action])
            else:
                if action == 'laser':
                    self.laser(direction, pos_player)
                elif action == 'feu':
                    self.feu(pos_player, direction)
                elif action == 'build':
                    self.build(pos_player, direction, obj_courant)
                elif action == 'sphere':
                    self.sphere(pos_player)
                elif action == 'conic':
                    self.conic(pos_player)
                self.add(-self.liste_mana_action[action])
                #pour eviter de perdre de la mana en créatif
                self.mana = 100 if not creatif else self.mana
        return None

    def laser(self, direction, pos_player):
        x_start = pos_player[0]

        for i in range(1, cst.taille_fenetre_largeur_win // 30 - x_start // 30):
            self.ecran.blit(self.dico_img['laser'][0], (i * 30 * direction + x_start, pos_player[1]))
            pygame.display.flip()
            self.carte.remove_bloc(self.carte.get_fov()[0] + x_start // 30 + i * direction, pos_player[1] // 30, '0')

    def feu(self, pos_player, direction):
        bloc = self.carte.get_tile(pos_player[0] // 30 + self.carte.get_fov()[0] + direction, pos_player[1] // 30)
        if bloc in self.blocs.list_fire():
            self.carte.fire_bloc(pos_player[0] // 30 + self.carte.get_fov()[0] + direction, pos_player[1] // 30)

    def build(self, pos_player, direction, obj_courant):
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #ATTENTION !!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #obj_courant sera le sceptre, il faudra demander à l'utilisateur de choisir un bloc autre !
        x = (pos_player[0] - 30) // 30 if direction == -1 else (pos_player[0] + 30) // 30
        end = abs(pos_player // 30 + 5) if abs(pos_player // 30 + 5) <= 20 else 20
        for i in range(abs(pos_player // 30 - 5), end):
            self.carte.remove_bloc(x + self.carte.get_fov()[0], i, obj_courant)

    def sphere(self, pos_player):
        vitesse = 5
        for i in range(-pos_player[1], 0, vitesse):
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0], abs(i) // 30, '0')
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0] + 1, abs(i) // 30, '0')
            self.carte.render()
            self.ecran.blit(self.dico_img['sphere'][0], (pos_player[0], abs(i)))
            pygame.display.flip()
        for i in range(0, 16 * 30, vitesse):
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0], abs(i) // 30, '0')
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0] + 1, abs(i) // 30, '0')
            self.carte.render()
            self.ecran.blit(self.dico_img['sphere'][0], (pos_player[0], abs(i)))
            pygame.display.flip()

    def conic(self, pos_player):
        vitesse = 5
        for i in range(-pos_player[1], 0, vitesse):
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0] - 1, abs(i) // 30, '0')
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0], abs(i) // 30, '0')
            self.carte.remove_bloc(pos_player[0] // 30 + self.carte.get_fov()[0] + 1, abs(i) // 30, '0')
            self.carte.render()
            self.ecran.blit(self.dico_img['conic'][0], (pos_player[0] - 30, abs(i)))
            pygame.display.flip()


class Personnage:
    def __init__(self, ecran, dossier, carte, rcenter, blocs, socket_serv=None, addr=('192.168.1.1', 60000), lan=False):
        self.x_pos = 0
        self.y_pos = 0
        self.ecran = ecran
        self.blocs = blocs
        self.socket_serv = socket_serv
        self.addr = addr
        self.location = dossier
        self.direction = "perso_droite.png"
        self.orientation = "droite"
        self.personnage_png = pygame.image.load("Personnage" + os.sep + self.location + self.direction).convert_alpha()
        self.carte = carte
        self.center = rcenter
        if not lan:
            self.vie = Vie(self.ecran, self.center)
        else:
            self.vie = LANVie(self.ecran, self.center, self.socket_serv, self.addr)
        self.mana = Mana(self.ecran, self.carte, self.blocs)
        self.speed = 60
        self.immobile = True
        self.immobile_time = 0
        self.pseudo = ""

    def get_dossier(self):
        return self.location

    def get_pseudo(self):
        return self.pseudo

    def set_pseudo(self, new):
        self.pseudo = new

    def get_speed(self):
        return self.speed

    def get_direction(self):
        return self.orientation

    def get_immobility(self):
        return self.immobile_time

    def set_speed(self, new):
        self.speed = new
        #vitesse du personnage réglé par celle des touches
        pygame.key.set_repeat(200, self.speed)

    def set_pos(self, new):
        self.x_pos = new[0]
        self.y_pos = new[1]

    def set_y(self, new_y):
        self.y_pos = new_y

    def set_x(self, new_x):
        self.x_pos = new_x

    def move(self, direction):
        self.orientation = direction
        self.immobile = False
        self.immobile_time = 0
        self.__deplacements(direction)
        self.immobile = True

    def __deplacements(self, direction):
        case_x = self.x_pos // 30 + self.carte.get_fov()[0]
        case_y = self.y_pos // 30
        last_fov = self.carte.get_fov()[0]

        if direction == 'haut':
            if case_y - 1 >= 0:
                if not self.carte.collide(case_x, case_y - 1):
                    case_y -= 1
        elif direction == 'gauche':
            if 0 <= case_x - 1:
                #escalier montant
                if self.carte.collide(case_x - 1, case_y) and not self.carte.collide(case_x, case_y - 1):
                    if 0 <= case_y - 1:
                        if not self.carte.collide(case_x - 1, case_y - 1):
                            if not self.carte.set_fov(self.carte.get_fov()[0] - 1, self.carte.get_fov()[1] - 1):
                                case_x -= 1
                            else:
                                case_y -= 1
                #déplacements normaux
                elif not self.carte.collide(case_x - 1, case_y):
                    if not self.carte.set_fov(self.carte.get_fov()[0] - 1, self.carte.get_fov()[1] - 1):
                        case_x -= 1
        elif direction == 'droite':
            if case_x + 1 <= 4096:
                #escalier montant
                if self.carte.collide(case_x + 1, case_y) and not self.carte.collide(case_x, case_y - 1):
                    if case_y - 1 >= 0:
                        if not self.carte.collide(case_x + 1, case_y - 1):
                            if not self.carte.set_fov(self.carte.get_fov()[0] + 1, self.carte.get_fov()[1] + 1) or self.x_pos // 30 < self.carte.get_space() // 5:
                                case_x += 1
                            else:
                                case_y -= 1
                #déplacements normaux
                elif not self.carte.collide(case_x + 1, case_y):
                    if not self.carte.set_fov(self.carte.get_fov()[0] + 1, self.carte.get_fov()[1] + 1):
                        case_x += 1
        self.x_pos = case_x - last_fov
        self.x_pos *= 30
        self.y_pos = case_y * 30

    def move_to_y(self, new_y):
        self.y_pos = new_y

    def move_to_x(self, new_x):
        self.x_pos = new_x

    def get_pos(self):
        return self.x_pos, self.y_pos

    def render(self):
        self.ecran.blit(self.personnage_png, (self.x_pos, self.y_pos))
        self.immobile_time += 1

    def change_direction(self, situation, mouse=False):
        if not mouse:
            self.direction = "perso_droite.png" if situation == "droite" else "perso_gauche.png"
            self.personnage_png = pygame.image.load("Personnage" + os.sep + self.location + self.direction).convert_alpha()

    def get_direction(self):
        return "droite" if self.direction == "perso_droite.png" else "gauche"

    def encaisser_degats(self, degats):
        self.vie.encaisser_degats(degats)

    def afficher_vie(self):
        self.vie.render()

    def afficher_mana(self):
        self.mana.render()

    def update_mana(self, quantity):
        self.mana.add(quantity)

    def regen_mana(self):
        self.mana.update()

    def set_mana(self, mana):
        self.mana.set(mana)

    def get_mana(self):
        return self.mana.get()

    def update_vie(self, ajouter_vie):
        self.vie.update(ajouter_vie)

    def mana_action(self, creatif, obj_courant, clic_pos):
        action = ''
        if obj_courant == 'D':
            action = 'laser'
        if obj_courant == 'F':
            action = 'teleporte'
        if obj_courant == 'G':
            action = 'feu'
        if obj_courant == 'H':
            action = 'conic'
        if obj_courant == 'J':
            action = 'sphere'
        if obj_courant == 'K':
            action = 'build'
        temp = self.mana.action(action, creatif, obj_courant, clic_pos, self.get_pos())
        if temp is not None:
            self.set_pos(temp)

    def set_vie(self, vie):
        self.vie.set(vie)

    def get_vie(self):
        return self.vie.get()