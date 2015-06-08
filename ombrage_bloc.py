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
    def __init__(self, ecran, base_type='nul'):
        self.ecran = ecran
        self.indice_shader = 0
        self.liste_shader = [
            'standart',
            'raycasté',
            'progressif',
            'gaussien',
            'nul'
        ]
        self.current_shader = base_type
        self.carte = []
        self.passe_a_travers = []
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(90)
        self.surf.convert_alpha()
        self.surf2 = self.surf
        self.ombre = False
        self.progressif = 0x000000
    
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
    
    def update(self, x=0, y=0):
        bloc = self.carte[y][x]
        if self.current_shader == 'standart':
            if bloc not in self.passe_a_travers:
                self.ecran.blit(self.surf, (x*30, y*30))
        if self.current_shader == 'raycasté':
            if bloc not in self.passe_a_travers:
                self.ombre = True
            if self.ombre:
                self.ecran.blit(self.surf, (x*30, y*30))
        if self.current_shader == 'progressif':
            if bloc not in self.passe_a_travers:
                self.progressif += 0x10
            else:
                self.progressif = 0x000000
            self.surf2.set_alpha(self.progressif)
            self.ecran.blit(self.surf2, (x*30, y*30))
        if self.current_shader == 'gaussien':
            pass


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
