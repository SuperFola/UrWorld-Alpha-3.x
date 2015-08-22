# -*-coding: utf8-*

import traceback
import pdb
import os


def pdb_post_mortem(exc_type, exc_val, exc_tb):
    # On affiche l'exception histoire de savoir ce qu'on debug
    print("".join(traceback.format_exception(exc_type, exc_val, exc_tb)))
    # On balance pdb en mode post mortem, c'est à dire qu'il va se lancer
    # malgré le fait que le programme ne marche plus, donnant accès
    # au contexte qu'il y avait juste avant que ça foire
    pdb.post_mortem(exc_tb)


# On dit à python de lancer cette fonction quand il plante, si on est pas sous Windows
if os.name != 'nt':
    sys.excepthook = pdb_post_mortem

VERSION = "Alpha 3.1.0"
finished = False

if not finished:
    import resize_with_pillow
    resize_with_pillow.start()


import glob
import sys
import text_entry
import restart
import compressor as rle
import dialog_box as dlb
from niveau import *
from tkinter import *
import math
import pickle
from gentest import *
import pygame
import time
from suite_jeu import *
from threading import Thread
import map_generator as map_gen
import parametrage as prm


#les blocks
blocs = Inventory()
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
blocs.add('404', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='404 Tile not found', tps_explode=0, take_fire=False)
blocs.add('ttt', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Horloge', tps_explode=0, take_fire=True)
blocs.add('lll', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Piston on', tps_explode=0, take_fire=False)
blocs.add('kkk', solid=True, shadow=0, gravity=False, quantity=10, innafichable=False, name='Piston collant on', tps_explode=0, take_fire=False)


largeur_dispo = cst.taille_fenetre_largeur_win

pas_de_partie = True

# Pas_de_partie changement d'affectation:
if os.path.exists(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "dossier.sav"):
    pas_de_partie = False
else:
    pas_de_partie = True


s = [
    ['h',  's',  'e',  'a',  'q',  'm',  't',  'd',  'r',  'y',  'u',  'i',  'M',  'v',  'l',  'k'],
    ['/',  '.',  '?',  'n',  'b',  'x',  'f',  'g',  'A',  'Z',  'E',  'R',  'T',  'Y',  'U',  'I'],
    ['O',  'P',  'Q',  'S',  'D',  'F',  'G',  'H',  'J',  'K',  'W',  'X',  'C',  'V',  'B',  'az'],
    ['ze', 'er', 'rt', 'ty', 'yu', 'ui', 'io', 'op', 'pq', 'qs', 'sd', 'df', 'fg', 'gh', 'hj', 'jk'],
    ['kl', 'lm', 'mw', 'wx', 'xc', 'cv', 'vb', 'bn', 'n?', '?.', './', '%a', '%b', 'aaa', 'bbb', 'ccc'],
    ['ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', '404', 'ttt', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['§%', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '/§']
]

print("Lancement du programme ...")

pygame.init()
root_ = None
fullscreen = True

if not finished:
    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "inventaire.sav", "wb") as i:
        pickle.Pickler(i).dump(s)
    root_ = pygame.display.set_mode((0, 0))  # definition de l'ecran principal
    fullscreen = False
else:
    root_ = pygame.display.set_mode((0, 0), FULLSCREEN)  # definition de l'ecran principal
    fullscreen = True

r = pygame.Rect(0, 0, largeur_dispo, 600)  # definition de la taille de la fenetre de jeu
r.center = root_.get_rect().center  # centrage de la fenetre par rapport a l'ecran total
fenetre = root_.subsurface(r)  # definition de la fenetre de jeu
fenetre.fill((60, 60, 60))  # coloriage de la fenetre de jeu en gris
pygame.display.update(r)  # mise a jour de la fenetre seulement
pygame.display.set_caption("UrWorld v." + VERSION)


def map_generator():
    generateur = map_gen.LaunchMapGen()
    generateur.generer()


thread_gen = Thread(target=map_generator)
thread_gen.start()

colors = [
    (255, 255, 255),  # blanc
    (255, 247, 30),  # jaune
    (255, 33, 255),  # rose
    (251, 148, 42),  # orange
    (253, 22, 76),  # rouge
    (205, 90, 173),  # violet
    (50, 205, 250),  # bleu
    (20, 255, 15),  # vert
    (160, 110, 44),  # marron
    (0, 0, 0)  # noir
]


def create_background(width, height):
    background = pygame.Surface((width, height))
    tile_width = 50
    y = 0
    while y < height:
        x = 0
        while x < width:
            row = y // tile_width
            col = x // tile_width
            pygame.draw.rect(
                background,
                colors[(row + col) % len(colors)],
                pygame.Rect(x, y, tile_width, tile_width))
            x += tile_width
        y += tile_width

    return background


def is_trying_to_quit(event, terminer_menu):
    pressed_keys = pygame.key.get_pressed()
    alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
    x_button = event.type == pygame.QUIT
    altF4 = alt_pressed and event.type == pygame.KEYDOWN and event.key == pygame.K_F4
    escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
    if terminer_menu is True:
        return x_button
    else:
        return x_button or altF4 or escape


def run_demos(width, height, fps):
    background = create_background(width, height)
    clock = pygame.time.Clock()
    the_world_is_a_happy_place = 0
    tmps_fin = time.time() + 2.5
    tmps_change_fond = time.time() + 0.25
    while True:
        the_world_is_a_happy_place += 1
        if os.path.exists(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl") \
                and open(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl", "rb").read() != "":
            if time.time() >= tmps_fin:
                break
        for event in pygame.event.get():
            if is_trying_to_quit(event, False):
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 5:  #la molette descend
                fps -= 5
            elif event.type == MOUSEBUTTONDOWN and event.button == 4:  #la molette monte
                fps += 5
        fenetre.blit(background, (0, 0))
        do_line_demo(fenetre, the_world_is_a_happy_place, background, fenetre)
        pygame.display.flip()
        clock.tick(fps)
        os_clear_command = 'cls' if sys.platform == 'win32' else 'clear'


def rotate_3d_points(points, angle_x, angle_y, angle_z, background, fenetre):
    font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 18)
    new_points = []
    for point in points:
        x = point[0]
        y = point[1]
        z = point[2]
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
        y = new_y
        # isn't math fun, kids?
        z = new_z
        new_x = x * math.cos(angle_y) - z * math.sin(angle_y)
        new_z = x * math.sin(angle_y) + z * math.cos(angle_y)
        x = new_x
        z = new_z
        new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
        new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
        x = new_x
        y = new_y
        new_points.append([x, y, z])
        _cX, _cY, _cZ = (x, y, z)
        _cX = math.fabs(_cX) * 50 - 1
        _cY = math.fabs(_cY) * 37.5 - 1
    return new_points


def do_line_demo(surface, counter, background, fenetre):
    logo_kubi = pygame.image.load(".." + os.sep + "assets" + os.sep + "Menu" + os.sep + "logo.png").convert_alpha()
    powered_by = pygame.image.load(".." + os.sep + "assets" + os.sep + "Menu" + os.sep + "pygame_powered.gif").convert_alpha()
    fenetre.blit(logo_kubi, ((largeur_dispo - 500) // 2, 10))
    fenetre.blit(powered_by, ((largeur_dispo - 250) // 2, cote_fenetre - 100))
    color = (0, 0, 0)
    cube_points = [[-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1], [1, -1, -1]]
    connections = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    t = counter * 2 * 3.141592653589 / 60  # this angle is 1 rotation per second

    # rotate about x axis every 2 seconds
    # rotate about y axis every 4 seconds
    # rotate about z axis every 6 seconds
    points = rotate_3d_points(cube_points, t / 2, t / 4, t / 6, background, fenetre)
    flattened_points = []
    for point in points:
        flattened_points.append(
            (point[0] * (1 + 1.0 / (point[2] + 3)),
             point[1] * (1 + 1.0 / (point[2] + 3))))

    for con in connections:
        p1 = flattened_points[con[0]]
        p2 = flattened_points[con[1]]
        x1 = p1[0] * 60 + (largeur_dispo / 2)
        y1 = p1[1] * 60 + (cote_fenetre / 2)
        x2 = p2[0] * 60 + (largeur_dispo / 2)
        y2 = p2[1] * 60 + (cote_fenetre / 2)
        # This is the only line that really matters
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), 4)


def reseau(surface, grd_font, hauteur_fen):
    data_serv = []
    dirt = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "dirt.png").convert()
    grass = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "herbe.png").convert()
    if os.path.exists(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "serveur.sav"):
        with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "serveur.sav", "rb") as serv_data_reading:
            data_serv = pickle.Unpickler(serv_data_reading).load()
    txt_reseau = grd_font.render("UrWorld - Réseau", 1, (240, 240, 240))
    width_ = 750
    height_ = 450
    continuer = 1
    choisi = -1
    largeur = 70
    hauteur = 50
    jouer_focus = False
    nouveau_focus = False
    menu_focus = False
    oublier_focus = False
    modifier_focus = False
    jouer_pos = (surface.get_size()[0] // 2 - largeur // 2, surface.get_size()[1] // 5 * 4)
    menu_pos = (surface.get_size()[0] // 2 + largeur // 2 + 20, surface.get_size()[1] // 5 * 4)
    nouveau_pos = (surface.get_size()[0] // 2 + width_ // 2 + 30, surface.get_size()[1] // 3)
    modifier_pos = (surface.get_size()[0] // 2 + width_ // 2 + 30, surface.get_size()[1] // 3 + hauteur + 20)
    oublier_pos = (surface.get_size()[0] // 2 + width_ // 2 + 30, surface.get_size()[1] // 3 + 2 * (hauteur + 20))
    jouer_couleur = (140, 140, 140) #(20, 180, 20)
    nouveau_couleur = (140, 140, 140) #(20, 20, 180)
    menu_couleur = (140, 140, 140) #(180, 20, 20)
    oublier_couleur = (140, 140, 140) #(180, 180, 20)
    modifier_couleur = (140, 140, 140) #(180, 20, 180)

    hote = ''
    port = 50000

    surf_noire = pygame.Surface((width_ - 20, 62))
    surf_noire.fill((76, 76, 76))
    surf_noire.set_alpha(80)
    surf_noire.convert_alpha()

    surf_verte = pygame.Surface((width_ - 20, 62))
    surf_verte.fill((20, 180, 20))
    surf_verte.set_alpha(80)
    surf_verte.convert_alpha()

    while continuer:
        jouer_couleur = (140, 140, 140) if not jouer_focus else (20, 180, 20)
        nouveau_couleur = (140, 140, 140) if not nouveau_focus else (20, 20, 180)
        menu_couleur = (140, 140, 140) if not menu_focus else (180, 20, 20)
        oublier_couleur = (140, 140, 140) if not oublier_focus else (180, 180, 20)
        modifier_couleur = (140, 140, 140) if not modifier_focus else (180, 20, 180)

        #le fond
        for i in range(largeur_dispo // 30 + 1):
            surface.blit(grass, (i * 30, 0))
            for j in range(surface.get_size()[1] // 30 - 1):
                surface.blit(dirt, (i * 30, (1 + j) * 30))
        #le titre
        surface.blit(txt_reseau, (surface.get_size()[0] // 2 - txt_reseau.get_size()[0] // 2, 3))

        #les boutons
        #bouton jouer
        pygame.draw.rect(surface, jouer_couleur, (jouer_pos[0], jouer_pos[1], largeur, hauteur))
        #bouton nouveau serveur
        pygame.draw.rect(surface, nouveau_couleur, (nouveau_pos[0], nouveau_pos[1], largeur + 30, hauteur))
        #bouton menu
        pygame.draw.rect(surface, menu_couleur, (menu_pos[0], menu_pos[1], largeur, hauteur))
        #bouton oublier un réseau
        pygame.draw.rect(surface, oublier_couleur, (oublier_pos[0], oublier_pos[1], largeur + 30, hauteur))
        #bouton modifier un réseau
        pygame.draw.rect(surface, modifier_couleur, (modifier_pos[0], modifier_pos[1], largeur + 30, hauteur))

        #les textes des boutons
        #texte jouer
        surface.blit(grd_font.render('Jouer', 1, (10, 10, 10)), (jouer_pos[0] + 6, jouer_pos[1] + 11))
        #texte nouveau serveur
        surface.blit(grd_font.render('Nouveau', 1, (10, 10, 10)), (nouveau_pos[0] + 6, nouveau_pos[1] + 11))
        #texte menu
        surface.blit(grd_font.render('Menu', 1, (10, 10, 10)), (menu_pos[0] + 8, menu_pos[1] + 11))
        #texte oublier un réseau
        surface.blit(grd_font.render('Oublier', 1, (10, 10, 10)), (oublier_pos[0] + 14, oublier_pos[1] + 11))
        #texte modifier un réseau
        surface.blit(grd_font.render('Modifier', 1, (10, 10, 10)), (modifier_pos[0] + 7, modifier_pos[1] + 11))

        #la liste déroulante des serveurs auxquels on s'est déjà connecté
        for i in range(len(data_serv)):
                if choisi == i:
                    surface.blit(surf_verte, (surface.get_size()[0] // 2 - width_ // 2 + 10,
                                                i * 64 + 60))
                else:
                        surface.blit(surf_noire, (surface.get_size()[0] // 2 - width_ // 2 + 10,
                                                    i * 64 + 60))
                nom_serv = grd_font.render(data_serv[i][1] + ' : ' + data_serv[i][0], 1, (10, 10, 10))
                description = grd_font.render(data_serv[i][2], 1, (10, 10, 10))
                surface.blit(nom_serv, (surface.get_size()[0] // 2 - width_ // 2 + 14,
                                        i * 64 + 62))
                surface.blit(description, (surface.get_size()[0] // 2 - width_ // 2 + 14,
                                           i * 64 + 64 + nom_serv.get_size()[1]))

        x_s, y_s = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    #clic LEFT
                    if menu_pos[0] <= x_s <= menu_pos[0] + largeur and menu_pos[1] + hauteur_fen <= y_s <= menu_pos[1] + hauteur_fen + hauteur:
                        continuer = 0
                    elif modifier_pos[0] <= x_s <= modifier_pos[0] + largeur + 30 and modifier_pos[1] + hauteur_fen <= y_s <= modifier_pos[1] + hauteur_fen + hauteur:
                        if 0 <= choisi <= len(data_serv) - 1:
                            new_params_co = dlb.DialogBox(surface, ["Entrez la nouvelle adresse IP suivie", "du port, le tout séparé par un ':' :"],
                                                      "Modification d'un serveur", (surface.get_size()[0] // 2, surface.get_size()[1] // 2),
                                                      grd_font, hauteur_fen, type_btn=2, mouse=False).render()
                            if re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,4}', new_params_co):
                                data_serv[choisi][0] = new_params_co
                            else:
                                dlb.DialogBox(surface, "Paramètre incorrect !", "Erreur",
                                              (surface.get_size()[0] // 2, surface.get_size()[1] // 2), grd_font,
                                              hauteur_fen, type_btn=0, mouse=False).render()
                    elif oublier_pos[0] <= x_s <= oublier_pos[0] + largeur + 30 and oublier_pos[1] + hauteur_fen <= y_s <= oublier_pos[1] + hauteur_fen + hauteur:
                        if 0 <= choisi <= len(data_serv) - 1:
                            effacer = dlb.DialogBox(surface, ["Voulez-vous vraiment oublier", "ce réseau ?"], "Supprimer le réseau", (surface.get_size()[0] // 2, surface.get_size()[1] // 2), grd_font, hauteur_fen, type_btn=1, mouse=False).render()
                            if effacer == 1:
                                #on efface le réseau
                                data_serv.pop(choisi)
                                dlb.DialogBox(surface, "Réseau effacé !", "Réseaux", (surface.get_size()[0] // 2, surface.get_size()[1] // 2), grd_font, hauteur_fen, type_btn=0, mouse=False).render()
                    elif jouer_pos[0] <= x_s <= jouer_pos[0] + largeur and jouer_pos[1] + hauteur_fen <= y_s <= jouer_pos[1] + hauteur_fen + hauteur:
                        if 0 <= choisi <= len(data_serv) - 1:
                            hote = data_serv[choisi][0].split(':')[0]
                            port = int(data_serv[choisi][0].split(':')[1])
                        with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "serveur.sav", "wb") as data_serv_wb:
                            pickle.Pickler(data_serv_wb).dump(data_serv)
                        return True, hote, port
                    elif nouveau_pos[0] <= x_s <= nouveau_pos[0] + largeur + 30 and nouveau_pos[1] + hauteur_fen <= y_s <= nouveau_pos[1] + hauteur_fen + hauteur:
                        if len(data_serv) < 6:
                            new_params_co = dlb.DialogBox(surface, ["Entrez l'adresse IP suivie du port,", "le tout séparé par un ':' :"],
                                                          "Ajout d'un serveur", (surface.get_size()[0] // 2, surface.get_size()[1] // 2),
                                                          grd_font, hauteur_fen, type_btn=2, mouse=False).render()
                            if re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{1,4}', new_params_co):
                                data_serv.append([new_params_co, "Nom (connectez vous au serveur pour l'obtenir)", "Description (même remarque)"])
                            else:
                                dlb.DialogBox(surface, "Paramètre incorrect !", "Erreur",
                                              (surface.get_size()[0] // 2, surface.get_size()[1] // 2), grd_font,
                                              hauteur_fen, type_btn=0, mouse=False).render()
                        else:
                                dlb.DialogBox(surface, ["Vous avez déjà atteint la limite de", "serveurs."], "Erreur",
                                              (surface.get_size()[0] // 2, surface.get_size()[1] // 2), grd_font,
                                              hauteur_fen, type_btn=0, mouse=False).render()
                    elif surface.get_size()[0] // 2 - width_ // 2 + 10 <= x_s <= surface.get_size()[0] // 2 + width_ // 2 - 10:
                        choisi = (y_s - 62 - hauteur_fen) // 64

        if jouer_pos[0] <= x_s <= jouer_pos[0] + largeur and jouer_pos[1] + hauteur_fen <= y_s <= jouer_pos[1] + hauteur_fen + hauteur:
            jouer_focus = True
        else:
            jouer_focus = False
        if nouveau_pos[0] <= x_s <= nouveau_pos[0] + largeur + 30 and nouveau_pos[1] + hauteur_fen <= y_s <= nouveau_pos[1] + hauteur_fen + hauteur:
            nouveau_focus = True
        else:
            nouveau_focus = False
        if menu_pos[0] <= x_s <= menu_pos[0] + largeur and menu_pos[1] + hauteur_fen <= y_s <= menu_pos[1] + hauteur_fen + hauteur:
            menu_focus = True
        else:
            menu_focus = False
        if oublier_pos[0] <= x_s <= oublier_pos[0] + largeur + 30 and oublier_pos[1] + hauteur_fen <= y_s <= oublier_pos[1] + hauteur_fen + hauteur:
            oublier_focus = True
        else:
            oublier_focus = False
        if modifier_pos[0] <= x_s <= modifier_pos[0] + largeur + 30 and modifier_pos[1] + hauteur_fen <= y_s <= modifier_pos[1] + hauteur_fen + hauteur:
            modifier_focus = True
        else:
            modifier_focus = False

        pygame.display.flip()

    with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "serveur.sav", "wb") as data_serv_wb:
        pickle.Pickler(data_serv_wb).dump(data_serv)

    return False, hote, port


creatif_choisi = True  # pas créatif en fait ;)
dossier_personnage = '0/'
pseudo = ""

if not pas_de_partie:
    with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pseudo.sav', 'r') as pseudo_lire:
        pseudo = pseudo_lire.read()
    with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'dossier.sav', 'rb') as dossier_lire:
        dossier_personnage = pickle.Unpickler(dossier_lire).load()
    #définition du mode de jeu ;)
    with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav', 'rb') as gamemode_r:
        creatif_choisi = pickle.Unpickler(gamemode_r).load()

font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 8)
grd_font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 12)
continuer2 = 1
couleurs = {
    'rouge': (180, 20, 20),
    'vert': (20, 180, 20)
}
largeur = 35
hauteur = 25
indice_dossier = 0
liste_dossier = [
    '1/',
    '2/',
    '3/',
    '4/',
    '5/',
    '6/',
    '7/',
    '8/'
]
dict_avatar = {
    '1/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '1' + os.sep + "perso_droite.png").convert_alpha(),
    '2/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '2' + os.sep + "perso_droite.png").convert_alpha(),
    '3/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '3' + os.sep + "perso_droite.png").convert_alpha(),
    '4/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '4' + os.sep + "perso_droite.png").convert_alpha(),
    '5/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '5' + os.sep + "perso_droite.png").convert_alpha(),
    '6/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '6' + os.sep + "perso_droite.png").convert_alpha(),
    '7/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '7' + os.sep + "perso_droite.png").convert_alpha(),
    '8/': pygame.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + '8' + os.sep + "perso_droite.png").convert_alpha()
}
milieu_screen = r.center[0] if r.center[0] == taille_fenetre_largeur_win // 2 else taille_fenetre_largeur_win // 2
bouton_creatif = (milieu_screen + 59, 304)
bouton_jouer = (milieu_screen - 2 * int(largeur * 1.25) - 40 - largeur * 2, 460 + hauteur * 3)
bouton_reseau = (milieu_screen - int(largeur * 1.25) - 30 - largeur, 460 + hauteur * 3)
bouton_quitter = (milieu_screen + 20 + 2 * int(largeur * 1.25), 460 + hauteur * 3)
bouton_effacer = (milieu_screen, 460 + hauteur * 3)
bouton_param = (milieu_screen * 2 - 20 - largeur * 4, 20)
couleur_btn_creatif = couleurs['vert'] if not creatif_choisi else couleurs['rouge']
couleur_btn_jouer = (140, 140, 140) #(20, 180, 20)
couleur_bouton_quitter = (140, 140, 140) #(180, 20, 20)
couleur_bouton_effacer = (140, 140, 140) #(20, 20, 180)
couleur_bouton_reseau = (140, 140, 140) #(180, 180, 20)
couleur_bouton_param = (140, 140, 140) #(180, 20, 180)
fond = pygame.image.load(random.choice(glob.glob(".." + os.sep + "assets" + os.sep + 'Menu' + os.sep + 'Fond' + os.sep + '*.png'))).convert()
pos_fd = (fenetre.get_rect().center[0] - (taille_fenetre_largeur_win + 450),
          fenetre.get_rect().center[1] - 800)
bouton_jouer_focus = False
bouton_quitter_focus = False
bouton_effacer_focus = False
bouton_reseau_focus = False
bouton_param_focus = False
hauteur_fenetre = (root_.get_size()[1] - 600) // 2
logo = pygame.image.load(".." + os.sep + "assets" + os.sep + "Menu" + os.sep + "URWORLD.png").convert_alpha()
text_box = text_entry.TextEntry((milieu_screen + 59, 200), fenetre)

if pas_de_partie or dossier_personnage == '0/':
    dossier_personnage = '1/'

########################################################################################################################
#à changer plus tard
########################################################################################################################
en_reseau = False
hote = '192.168.1.0'
port = 50000
realistic = False

avatar = pygame.image.load(".." + os.sep + "assets" + os.sep + 'Personnage' + os.sep + dossier_personnage + 'perso_droite.png').convert_alpha()

val_retour = 0

"""
                 moi        -> alpha
r.center      :: (683, 384) -> (960, 540)
screen width  :: 1366       -> 1280
middle screen :: 683        -> 640
probleme      ::               îîî
"""

while continuer2:
    #mise à jour des variables
    texte_btn_creatif = 'Oui' if not creatif_choisi else 'Non'
    # Pas_de_partie changement d'affectation:
    if os.path.exists(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "dossier.sav"):
        pas_de_partie = False
    else:
        pas_de_partie = True
    if pas_de_partie:
        pseudo = text_box.value()
    couleur_btn_jouer = (140, 140, 140) if not bouton_jouer_focus else (20, 180, 20)
    couleur_bouton_quitter = (140, 140, 140) if not bouton_quitter_focus else (180, 20, 20)
    couleur_bouton_effacer = (140, 140, 140) if not bouton_effacer_focus else (20, 20, 180)
    couleur_bouton_reseau = (140, 140, 140) if not bouton_reseau_focus else (180, 180, 20)
    couleur_bouton_param = (140, 140, 140) if not bouton_param_focus else (180, 20, 180)

    #deplacement du fond
    movement = pygame.mouse.get_rel()
    pos_fd = (pos_fd[0] - movement[0], pos_fd[1] - movement[1])

    #mise à jour des surfaces
    #fond
    fenetre.blit(fond, pos_fd)
    #logo
    fenetre.blit(logo, (milieu_screen - logo.get_size()[0] // 2, 10))
    #les différentes sections
    fenetre.blit(grd_font.render("Créatif :: ", 1, (10, 10, 10)), (milieu_screen - 2 * largeur, bouton_creatif[1]))
    fenetre.blit(grd_font.render("Pseudo  :: ", 1, (10, 10, 10)), (milieu_screen - 2 * largeur, 200))
    #bouton creatif
    pygame.draw.rect(fenetre, couleur_btn_creatif, (bouton_creatif[0],
                                                    bouton_creatif[1],
                                                    largeur,
                                                    hauteur))
    #bouton jouer
    pygame.draw.rect(fenetre, couleur_btn_jouer, (bouton_jouer[0],
                                              bouton_jouer[1],
                                              largeur * 2,
                                              hauteur * 2))
    #bouton reseau
    pygame.draw.rect(fenetre, couleur_bouton_reseau, (bouton_reseau[0],
                                                    bouton_reseau[1],
                                                    int(largeur * 2.5),
                                                    hauteur * 2))
    #bouton quitter
    pygame.draw.rect(fenetre, couleur_bouton_quitter, (bouton_quitter[0],
                                                    bouton_quitter[1],
                                                    largeur * 2 + 10,
                                                    hauteur * 2))

    #bouton effacer (la partie)
    pygame.draw.rect(fenetre, couleur_bouton_effacer, (bouton_effacer[0],
                                                    bouton_effacer[1],
                                                    int(largeur * 2.5),
                                                    hauteur * 2))
    #bouton parametres
    pygame.draw.rect(fenetre, couleur_bouton_param, (bouton_param[0],
                                                     bouton_param[1],
                                                     largeur * 4,
                                                     hauteur * 2))

    #bouton -1 pour le choix de l'avatar
    pygame.draw.rect(fenetre, (20, 180, 20), (milieu_screen + 40,
                                              264,
                                              15,
                                              30))
    #bouton +1 pour le choix de l'avatar
    pygame.draw.rect(fenetre, (20, 180, 20), (milieu_screen + 85,
                                              264,
                                              15,
                                              30))
    #textes
    #texte bouton creatif
    fenetre.blit(font.render(texte_btn_creatif, 1, (10, 10, 10)), (bouton_creatif[0] + 6, bouton_creatif[1] + 4))
    #texte bouton jouer
    fenetre.blit(grd_font.render('Jouer', 1, (10, 10, 10)), (bouton_jouer[0] + 6, bouton_jouer[1] + 11))
    #texte bouton reseau
    fenetre.blit(grd_font.render('Réseau', 1, (10, 10, 10)), (bouton_reseau[0] + 6, bouton_reseau[1] + 11))
    #texte bouton quitter
    fenetre.blit(grd_font.render('Quitter', 1, (10, 10, 10)), (bouton_quitter[0] + 6, bouton_quitter[1] + 11))
    #texte bouton effacer (la partie)
    fenetre.blit(grd_font.render('Effacer', 1, (10, 10, 10)), (bouton_effacer[0] + 6, bouton_effacer[1] + 11))
    #texte section avatar
    fenetre.blit(grd_font.render('Avatar :: ', 1, (10, 10, 10)), (milieu_screen - 2 * largeur, 264))
    #texte section année
    fenetre.blit(grd_font.render('Année :: ', 1, (10, 10, 10)), (milieu_screen - 2 * largeur, 230))
    fenetre.blit(grd_font.render(str(len(glob.glob('Niveaux' + os.sep + 'Olds Maps' + os.sep + '*.lvl'))),
                                 1, (10, 10, 10)), (milieu_screen + 30, 230))
    #texte bouton parametres
    fenetre.blit(grd_font.render('Paramètres', 1, (10, 10, 10)), (bouton_param[0] + 13, bouton_param[1] + 11))
    #texte bouton +1 / -1 dossier perso
    fenetre.blit(font.render("<", 1, (10, 10, 10)), (milieu_screen + 43, 268))
    fenetre.blit(font.render(">", 1, (10, 10, 10)), (milieu_screen + 90, 268))

    #avatar
    fenetre.blit(avatar, (milieu_screen + 55, 264))

    #les events
    for e in pygame.event.get():
        if e.type == QUIT:
            continuer2 = 0
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                continuer2 = 0
            else:
                if pas_de_partie:
                    text_box.add_letter(e)
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                #clic gauche
                #bouton créatif
                if bouton_creatif[0] <= e.pos[0] <= bouton_creatif[0] + largeur \
                    and bouton_creatif[1] + hauteur_fenetre <= e.pos[1] <= bouton_creatif[1] + hauteur + hauteur_fenetre:
                    creatif_choisi = not creatif_choisi
                    couleur_btn_creatif = couleurs['vert'] if not creatif_choisi else couleurs['rouge']
                #bouton reseau
                elif bouton_reseau[0] <= e.pos[0] <= bouton_reseau[0] + largeur * 2 \
                    and bouton_reseau[1] + hauteur_fenetre <= e.pos[1] <= bouton_jouer[1] + hauteur_fenetre + hauteur * 2:
                    en_reseau, hote, port = reseau(fenetre, grd_font, hauteur_fenetre)
                    if en_reseau:
                        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav', 'wb') as gamemode_w:
                            pickle.Pickler(gamemode_w).dump(creatif_choisi)
                        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pseudo.sav', 'w') as pseudo_w:
                            pseudo_w.write(pseudo)
                        #on génére une map dans ce cas
                        if val_retour == 1:
                            thread_gen = Thread(target=map_generator)
                            thread_gen.start()
                        #on lance le jeu
                        run_demos(largeur_dispo, cote_fenetre, 60)
                        jeu(hote, port, en_reseau, root_, fenetre, creatif_choisi, dossier_personnage, r.center, blocs, hauteur_fenetre)
                        pygame.mouse.set_visible(True)
                #bouton jouer
                elif bouton_jouer[0] <= e.pos[0] <= bouton_jouer[0] + largeur * 2 \
                    and bouton_jouer[1] + hauteur_fenetre <= e.pos[1] <= bouton_jouer[1] + hauteur * 2 + hauteur_fenetre:
                        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav', 'wb') as gamemode_w:
                            pickle.Pickler(gamemode_w).dump(creatif_choisi)
                        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pseudo.sav', 'w') as pseudo_w:
                            pseudo_w.write(pseudo)
                        #on génére une map dans ce cas
                        if val_retour == 1:
                            thread_gen = Thread(target=map_generator)
                            thread_gen.start()
                        #on lance le jeu
                        run_demos(largeur_dispo, cote_fenetre, 60)
                        jeu(hote, port, en_reseau, root_, fenetre, creatif_choisi, dossier_personnage, r.center, blocs, hauteur_fenetre)
                        pygame.mouse.set_visible(True)
                #bouton paramètres
                elif bouton_param[0] <= e.pos[0] <= bouton_param[0] + largeur * 4 \
                    and bouton_param[1] + hauteur_fenetre <= e.pos[1] <= bouton_param[1] + hauteur_fenetre + hauteur * 2:
                    prm.parametres(fenetre, grd_font, hauteur_fenetre, fullscreen)
                #bouton quitter
                elif bouton_quitter[0] <= e.pos[0] <= bouton_quitter[0] + largeur * 2 \
                    and bouton_quitter[1] + hauteur_fenetre <= e.pos[1] <= bouton_quitter[1] + hauteur_fenetre + hauteur * 2:
                    sys.exit()
                #bouton effacer (la partie)
                elif bouton_effacer[0] <= e.pos[0] <= bouton_effacer[0] + int(largeur * 2.5) \
                    and bouton_effacer[1] + hauteur_fenetre <= e.pos[1] <= bouton_effacer[1] + hauteur_fenetre + hauteur * 2:
                    val_retour = dlb.DialogBox(fenetre, 'Voulez-vous continuer ?', 'Effacer la partie', r.center,
                                               grd_font, hauteur_fenetre, type_btn=1, mouse=False).render()
                    if val_retour == 1:
                        restart.restart()
                        dlb.DialogBox(fenetre, 'Partie effacée !', 'Nouvelle partie', r.center, grd_font,
                                      hauteur_fenetre, type_btn=0, mouse=False).render()
                #bouton -1 dossier personnage
                elif milieu_screen + 40 <= e.pos[0] <= milieu_screen + 55 \
                    and 384 + hauteur_fenetre - 120 <= e.pos[1] <= 384 + hauteur_fenetre - 90:
                    indice_dossier = indice_dossier - 1 if indice_dossier - 1 >= 0 else 0
                    dossier_personnage = liste_dossier[indice_dossier]
                    avatar = dict_avatar[liste_dossier[indice_dossier]]
                #bouton +1 dossier personnage
                elif milieu_screen + 85 <= e.pos[0] <= milieu_screen + 100 \
                    and 384 + hauteur_fenetre - 120 <= e.pos[1] <= 384 + hauteur_fenetre - 90:
                    indice_dossier = indice_dossier + 1 if indice_dossier + 1 <= len(liste_dossier) - 1 else len(liste_dossier) - 1
                    dossier_personnage = liste_dossier[indice_dossier]
                    avatar = dict_avatar[liste_dossier[indice_dossier]]
    if pas_de_partie:
        text_box.render()
    else:
        fenetre.blit(grd_font.render("` " + pseudo + " `", 1, (10, 10, 10)), (milieu_screen + 59, 200))
    #"mousemotion"
    if bouton_jouer[0] <= pygame.mouse.get_pos()[0] <= bouton_jouer[0] + largeur * 2 \
        and bouton_jouer[1] + hauteur_fenetre <= pygame.mouse.get_pos()[1] <= bouton_jouer[1] + hauteur_fenetre + hauteur * 2:
        bouton_jouer_focus = True
    else:
        bouton_jouer_focus = False
    if bouton_quitter[0] <= pygame.mouse.get_pos()[0] <= bouton_quitter[0] + largeur * 2 \
        and bouton_quitter[1] + hauteur_fenetre <= pygame.mouse.get_pos()[1] <= bouton_quitter[1] + hauteur_fenetre + hauteur * 2:
        bouton_quitter_focus = True
    else:
        bouton_quitter_focus = False
    if bouton_effacer[0] <= pygame.mouse.get_pos()[0] <= bouton_effacer[0] + int(largeur * 2.5) \
        and bouton_effacer[1] + hauteur_fenetre <= pygame.mouse.get_pos()[1] <= bouton_effacer[1] + hauteur_fenetre + hauteur * 2:
        bouton_effacer_focus = True
    else:
        bouton_effacer_focus = False
    if bouton_reseau[0] <= pygame.mouse.get_pos()[0] <= bouton_reseau[0] + int(largeur * 2.5) \
        and bouton_reseau[1] + hauteur_fenetre <= pygame.mouse.get_pos()[1] <= bouton_reseau[1] + hauteur_fenetre + hauteur * 2:
        bouton_reseau_focus = True
    else:
        bouton_reseau_focus = False
    if bouton_param[0] <= pygame.mouse.get_pos()[0] <= bouton_param[0] + largeur * 4 \
        and bouton_param[1] + hauteur_fenetre <= pygame.mouse.get_pos()[1] <= bouton_param[1] + hauteur_fenetre + hauteur * 2:
        bouton_param_focus = True
    else:
        bouton_param_focus = False

    #mise à jour de l'écran
    pygame.display.flip()