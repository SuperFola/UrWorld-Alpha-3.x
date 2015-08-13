import pygame
from tkinter import *
import os
from pygame.locals import *
import constantes as cst

#constants
TILE_TAILLE = 30

# level dimensions
height = 20
taille_fenetre_largeur_win = cst.taille_fenetre_largeur_win
width = taille_fenetre_largeur_win // 30 + 30


class Shader:
    def __init__(self, ecran, blocs, base_type='standart'):
        self.ecran = ecran
        self.indice_shader = 0
        self.liste_shader = [
            'standart',
            'raycasté',
            'progressif',
            'nul'
        ]
        self.blocs = blocs
        self.current_shader = base_type
        self.carte = []
        self.blocs_passe_pas = self.blocs.list_solid()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(90)
        self.surf.convert_alpha()
        self.surfs = []
        self.surf2 = pygame.Surface((30, 30))
        self.surf2.fill((0, 0, 0))
        self.surf2.set_alpha(90)
        self.surf2.convert_alpha()
        self.ombre = False
        self.progressif = 0x000000
        self.max_time_game = 0

    def set_max_time_game(self, value):
        #a appeler au plus tot, car crée les surfaces pour le shader std !!
        self.max_time_game = value
        self.generate()

    def generate(self):
        surf = pygame.Surface((30, 30))
        surf.fill((0, 0, 0))
        magic_constant = 4.5
        for i in range(self.max_time_game):
            surf.set_alpha(int(i * magic_constant))
            surf.convert_alpha()
            self.surfs.append([surf, int(i * magic_constant)])

    def get_std_shade(self, game_time):
        return self.surfs[game_time][1]
    
    def change_shader(self):
        self.indice_shader += 1
        self.current_shader = self.liste_shader[self.indice_shader % len(self.liste_shader)]
    
    def create(self, carte):
        self.carte = carte
        self.progressif = 0x000000
        self.ombre = False
    
    def get_cur_shader(self):
        return self.current_shader
    
    def set_shader(self, new):
        self.current_shader = new
    
    def update(self, x=0, y=0, time_game=0):
        bloc = self.carte[y][x]
        if not y:
            self.ombre = False
            self.progressif = 0x000000
        if self.current_shader == 'standart':
            if bloc in self.blocs_passe_pas:
                self.ecran.blit(self.surfs[time_game][0], (x*30, y*30))
        if self.current_shader == 'raycasté':
            if bloc in self.blocs_passe_pas:
                self.ombre = True
            if self.ombre:
                self.ecran.blit(self.surf, (x*30, y*30))
        if self.current_shader == 'progressif':
            cur_case_ombre = 0
            if bloc in self.blocs_passe_pas:
                if x - 1 >= 0 and x + 1 <= len(self.carte[0]) - 1:
                    if self.carte[y][x-1] in self.blocs_passe_pas and self.carte[y][x+1] not in self.blocs_passe_pas:
                        cur_case_ombre += 32
                    if self.carte[y][x-1] not in self.blocs_passe_pas and self.carte[y][x+1] not in self.blocs_passe_pas:
                        cur_case_ombre += 16
                    if self.carte[y][x-1] not in self.blocs_passe_pas and self.carte[y][x+1] in self.blocs_passe_pas:
                        cur_case_ombre += 32
                    if self.carte[y][x-1] in self.blocs_passe_pas and self.carte[y][x+1] in self.blocs_passe_pas:
                        cur_case_ombre += 64
                if x - 1 < 0:
                    if self.carte[y][x+1] not in self.blocs_passe_pas:
                        cur_case_ombre += 16
                    else:
                        cur_case_ombre += 32
                if x + 1 > len(self.carte[0]) - 1:
                    if self.carte[y][x-1] not in self.blocs_passe_pas:
                        cur_case_ombre += 16
                    else:
                        cur_case_ombre += 32
                self.progressif += 8
            else:
                self.progressif = 0x000000
            self.surf2.set_alpha(self.progressif + cur_case_ombre)
            self.ecran.blit(self.surf2, (x*30, y*30))


def distance_right(x, y, carte, fov):
    distance = 0

    for i in range(x, fov[1] - fov[0]):
        bloc = carte[y][i]
        if bloc == '0':
            break
        else:
            distance += 1

    return distance


def distance_left(x, y, carte, fov):
    distance = 0

    for i in range(x, fov[1] - fov[0]):
        j = (fov[1] - fov[0]) - i
        bloc = carte[y][j]
        if bloc == '0':
            break
        else:
            distance += 1

    return distance


distance_top = lambda x, y, struc: len([line[x] for line in struc[y::-1] if line[x] != '0'])
distance_bottom = lambda x, y, struc: len([line[x] for line in struc[y::] if line[x] != '0'])


def get_minus(*args):
    nombre = 0x000000 + 0x10 * 20
    for i in args:
        nombre = i if i <= nombre else nombre
    return nombre


def ombrage_bloc(fenetre, structure_niv, fov, blocs):
    surf = pygame.Surface((30, 30))
    surf.fill(0x000000)
    surf.set_alpha(80)
    surf.convert_alpha()

    for x in range(fov[1] - fov[0]):
        for y in range(20):
            case = structure_niv[y][x]
            if case in blocs.list_solid():
                fenetre.blit(surf, (x * TILE_TAILLE, y * TILE_TAILLE))


def ombrage_bloc2(fenetre, structure_niveau, fov, blocs):
    obscurite = 0x000000

    for x in range(fov[1] - fov[0]):
        for y in range(20):
            bloc = structure_niveau[y][x]

            if bloc in blocs.list_solid():
                obscurite += 0x10
            else:
                obscurite = 0x000000
            surf = pygame.Surface((30, 30))
            surf.fill(0x000000)
            surf.set_alpha(obscurite)
            surf.convert_alpha()
            fenetre.blit(surf, (x * 30, y * 30))


def ombrage_bloc3(fenetre, structure_niveau, fov, blocs):
    surf = pygame.Surface((30, 30))
    surf.fill(0x000000)
    surf.set_alpha(60)
    surf.convert_alpha()

    for x in range(fov[1] - fov[0]):
        lumiere = True
        for y in range(20):
            bloc = structure_niveau[y][x]

            if bloc in blocs.list_solid():
                lumiere = False
            if not lumiere:
                fenetre.blit(surf, (x * 30, y * 30))


def ombrage_bloc4(fenetre, structure_niveau, fov, blocs):
    obscurite = 0x000000

    for x in range(fov[1] - fov[0]):
        lumiere = True
        for y in range(20):
            bloc = structure_niveau[y][x]
            if bloc in blocs.list_solid():
                obscurite += 0x10

            if bloc in blocs.list_solid():
                lumiere = False
            if not lumiere:
                surf = pygame.Surface((30, 30))
                surf.fill(0x000000)
                surf.set_alpha(obscurite)
                surf.convert_alpha()
                fenetre.blit(surf, (x * 30, y * 30))
        obscurite = 0x000000
