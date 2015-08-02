# -*-coding: utf8-*

import sys
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
    ['ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', '404', '0', '0', '0', '0', '0', '0', '0', '0'],
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


def texture_pack(fenetre, grd_font, hauteur_fen, fullscreen):
    path_to = dlb.DialogBox(fenetre, ["Chemin vers le pack de", "textures :"], "Pack de textures",
                            (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                            type_btn=2, mouse=False).render()
    if path_to != '':
        if os.path.exists(path_to):
            with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'texture_pack.sav', 'w') as txt_pack_w:
                txt_pack_w.write(path_to + os.sep)
        else:
            dlb.DialogBox(fenetre, ["Erreur dans le chemin", "vers la pack de textures"], "Erreur",
                          (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                           type_btn=2, mouse=False).render()
    return fullscreen


def fov_size(fenetre, grd_font, hauteur_fen, fullscreen):
    new_size = dlb.DialogBox(fenetre, ["Nouvelle taille pour le FOV,", "comprise entre 0 et 75 :"], "Taille du FOV",
                            (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                            type_btn=3, mouse=False).render()
    if new_size != '':
        if int(new_size) > 0:
            last_size = [0, 0]
            with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'fov.sav', 'rb') as fovrb:
                last_size = pickle.Unpickler(fovrb).load()
            if last_size[0] + int(new_size) < 4096:
                with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'fov.sav', 'wb') as fovwb:
                    pickle.Pickler(fovwb).dump([last_size[0], last_size[0] + int(new_size)])
    return fullscreen


def jump_height(fenetre, grd_font, hauteur_fen, fullscreen):
    height_jump = dlb.DialogBox(fenetre, "Hauteur du saut (en case) :", "Saut",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if height_jump != '':
        if 0 < int(height_jump) <= 16:
            with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'jheight.sav', 'w') as jhw:
                jhw.write(str(height_jump))
    return fullscreen


def jump_time(fenetre, grd_font, hauteur_fen, fullscreen):
    time_jump = dlb.DialogBox(fenetre, "Temps du saut (en millisecondes) :", "Saut",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if time_jump != '':
        if 0 < int(time_jump) <= 512:
            with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'jtime.sav', 'w') as tjw:
                tjw.write(str(time_jump))
    return fullscreen


def gamemode_def(fenetre, grd_font, hauteur_fen, fullscreen):
    last_gm = ""
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav', 'rb') as gmr:
            last_gm = pickle.Unpickler(gmr).load()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamemode.sav', 'wb') as gmw:
            pickle.Pickler(gmw).dump(not last_gm)
        value_of = "Créatif" if last_gm else "Survie"
        dlb.DialogBox(fenetre, ["Votre mode de jeu a bien été changé", "est : " + value_of], "Mode de jeu",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Le fichier permettant la manipulation", "n'existe pas."], "Erreur",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    return fullscreen


def bg_color(fenetre, grd_font, hauteur_fen, fullscreen):
    couleur = dlb.DialogBox(fenetre, ["Code couleur (sous la forme :", "(Red, Green, Blue))"], "Couleur de fond",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=2, mouse=False).render()
    if couleur != '':
        if re.match(r'\([0-9]{1,3}, ? ?[0-9]{1,3}, ?[0-9]{1,3}\)', couleur):
            with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'couleur.sav', 'w') as clw:
                clw.write(str(couleur))
        else:
            dlb.DialogBox(fenetre, ["Le code couleur fournit n'est pas", "valide dans son contexte."], "Erreur",
                                    (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                    type_btn=0, mouse=False).render()
    return fullscreen


def windows_property(fenetre, grd_font, hauteur_fen, fullscreen):
    root_ = None
    if fullscreen:
        root_ = pygame.display.set_mode((0, 0))  #definition de l'ecran principal
    else:
        root_ = pygame.display.set_mode((0, 0), FULLSCREEN)  #definition de l'ecran principal
    r = pygame.Rect(0, 0, largeur_dispo, 600)  #definition de la taille de la fenetre de jeu
    r.center = root_.get_rect().center  #centrage de la fenetre par rapport a l'ecran total
    fenetre = root_.subsurface(r)  #definition de la fenetre de jeu
    fenetre.fill((60, 60, 60))  #coloriage de la fenetre de jeu en gris
    pygame.display.update(r)  #mise a jour de la fenetre seulement
    return not fullscreen


def vent_property(fenetre, grd_font, hauteur_fen, fullscreen):
    last_wind = ""
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav', 'rb') as vprb:
            last_wind = pickle.Unpickler(vprb).load()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav', 'wb') as vpwb:
            pickle.Pickler(vpwb).dump(not last_wind)
        dlb.DialogBox(fenetre, ["Le vent est désormais ", "actif" if not last_wind else "nul"], "Vent",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Le fichier permettant la manipulation", "n'existe pas et va être créé."], "Erreur",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'vent.sav', 'wb') as vpwbt:
            pickle.Pickler(vpwbt).dump(False)

    return fullscreen


def pluie_property(fenetre, grd_font, hauteur_fen, fullscreen):
    last_rain = ""
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav', 'rb') as pprb:
            last_rain = pickle.Unpickler(pprb).load()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav', 'wb') as ppwb:
            pickle.Pickler(ppwb).dump(not last_rain)
        dlb.DialogBox(fenetre, ["La pluie est désormais ", "active" if not last_rain else "nulle"], "Pluie",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Le fichier permettant la manipulation", "n'existe pas et va être créé."], "Erreur",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'pluie.sav', 'wb') as ppwbt:
            pickle.Pickler(ppwbt).dump(False)

    return fullscreen


def orage_property(fenetre, grd_font, hauteur_fen, fullscreen):
    last_orage = ""
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav', 'rb') as oprb:
            last_orage = pickle.Unpickler(oprb).load()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav', 'wb') as opwb:
            pickle.Pickler(opwb).dump(not last_orage)
        dlb.DialogBox(fenetre, ["L'orage est désormais ", "actif" if not last_orage else "nul"], "Orage",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Le fichier permettant la manipulation", "n'existe pas et va être créé."], "Erreur",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'orage.sav', 'wb') as opwbt:
            pickle.Pickler(opwbt).dump(False)

    return fullscreen


def clouds_property(fenetre, grd_font, hauteur_fen, fullscreen):
    last_cloud = ""
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'clouds.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'clouds.sav', 'rb') as cprb:
            last_cloud = pickle.Unpickler(cprb).load()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'clouds.sav', 'wb') as cpwb:
            pickle.Pickler(cpwb).dump(not last_cloud)
        dlb.DialogBox(fenetre, ["Les nuages sont désormais ", "visibles" if not last_cloud else "invisibles"], "Nuages",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Le fichier permettant la manipulation", "n'existe pas et va être créé."], "Erreur",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'clouds.sav', 'wb') as cpwbt:
            pickle.Pickler(cpwbt).dump(False)

    return fullscreen


def height_map(fenetre, grd_font, hauteur_fen, fullscreen):
    height = dlb.DialogBox(fenetre, ["Hauteur de la map (defaut:20)"], "Map",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if height.isdigit():
        with open(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + 'height_map.sav', 'wb') as file:
            pickle.Pickler(file).dump(height)

    return fullscreen


def flatness_map(fenetre, grd_font, hauteur_fen, fullscreen):
    flat = dlb.DialogBox(fenetre, ["Planéité de la map (defaut:4)"], "Map",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if flat.isdigit():
        with open(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + 'flatness_map.sav', 'wb') as file:
            pickle.Pickler(file).dump(flat)

    return fullscreen


def deniv_map(fenetre, grd_font, hauteur_fen, fullscreen):
    deniv = dlb.DialogBox(fenetre, ["Dénivelé de la map (defaut:1)"], "Map",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if deniv.isdigit():
        with open(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + 'deniv_map.sav', 'wb') as file:
            pickle.Pickler(file).dump(deniv)

    return fullscreen


def headstart_map(fenetre, grd_font, hauteur_fen, fullscreen):
    headstart = dlb.DialogBox(fenetre, ["Hauteur de la 1ere colonne (defaut:10)", "Doit être inférieur", "à la hauteur de la carte"], "Map",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if headstart.isdigit():
        with open(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + 'headstart_map.sav', 'wb') as file:
            pickle.Pickler(file).dump(headstart)

    return fullscreen


def lenght_map(fenetre, grd_font, hauteur_fen, fullscreen):
    lenght = dlb.DialogBox(fenetre, ["Taille de la map (defaut:4096)", "Doit être un multiple", "de 2 (1024, 2048 ...)"], "Map",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=3, mouse=False).render()
    if lenght.isdigit():
        with open(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + 'lenght_map.sav', 'wb') as file:
            pickle.Pickler(file).dump(lenght)

    return fullscreen


def pass_(fenetre, grd_font, hauteur_fen, fullscreen):
    return fullscreen


def parametres(fenetre, grd_font, hauteur_fenetre, fullscreen):
    txt_path = ".." + os.sep + "assets" + os.sep + "Tiles" + os.sep
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'texture_pack.sav'):
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'texture_pack.sav', 'r') as txt_pack_r:
            txt_path = txt_pack_r.read()
    stone = pygame.image.load(txt_path + "pierre.png").convert()
    snow = pygame.image.load(txt_path + "neige.png").convert()
    diamond = pygame.image.load(txt_path + "mine_diamant.png").convert()
    rubis = pygame.image.load(txt_path + "mine_rubis.png").convert()
    emeraude = pygame.image.load(txt_path + "mine_emeraude.png").convert()
    or_ = pygame.image.load(txt_path + "mine_or.png").convert()
    charbon = pygame.image.load(txt_path + "mine_charbon.png").convert()
    lst_surf = [stone] * 50 + [diamond, rubis, emeraude, or_, charbon]
    titre = grd_font.render('Paramètres', 1, (10, 10, 10))
    liste_commandes = ''
    with open(".." + os.sep + "assets" + os.sep + 'Menu' + os.sep + 'commands.txt', 'r') as file:
        liste_commandes = file.readlines()
    surf_noire = pygame.Surface((400, fenetre.get_size()[1] - 90))
    surf_noire.fill(0x000000)
    surf_noire.set_alpha(80)
    surf_noire.convert_alpha()
    surf_noire2 = pygame.Surface((400, fenetre.get_size()[1] - 160))
    surf_noire2.fill(0x000000)
    surf_noire2.set_alpha(80)
    surf_noire2.convert_alpha()
    continuer = 1
    danger_color = (170, 15, 15)
    normal_color = (10, 10, 10)
    clikable = [
        ['Pack de textures', texture_pack, normal_color],
        ['Taille du FOV', fov_size, normal_color],
        ['Hauteur du saut', jump_height, normal_color],
        ['Temps de saut', jump_time, normal_color],
        ['Mode de jeu', gamemode_def, normal_color],
        ['Couleur de fond', bg_color, normal_color],
        ['Etat de la fenetre', windows_property, normal_color],
        ['Vent', vent_property, normal_color],
        ['Pluie', pluie_property, normal_color],
        ['Orage', orage_property, normal_color],
        ['Nuages', clouds_property, normal_color],
        ['Hauteur de la map (defaut:20)', height_map, danger_color],
        ['Planéité de la map (defaut:4)', flatness_map, danger_color],
        ['Dénivelé (defaut:1)', deniv_map, danger_color],
        ['Hauteur de la 1ere colonne (defaut:10)', headstart_map, danger_color],
        ['Taille de la map (defaut:4096)', lenght_map, danger_color],
        ['', pass_, normal_color],
        ['', pass_, normal_color],
        ['', pass_, normal_color],
        ['', pass_, normal_color],
        ['', pass_, normal_color]
    ]
    btn_menu_focus = False
    largeur = 70
    hauteur = 50
    btn_menu_pos = (fenetre.get_size()[0] - 20 - largeur, fenetre.get_size()[1] - 20 - hauteur)
    fond = pygame.Surface((fenetre.get_size()[0], fenetre.get_size()[1]))
    #le fond
    for i in range(fenetre.get_size()[0] // 30 + 1):
        fond.blit(snow, (i * 30, 0))
        for j in range(fenetre.get_size()[1] // 30 - 1):
            fond.blit(random.choice(lst_surf), (i * 30, (j + 1) * 30))

    while continuer:
        btn_menu_color = (180, 20, 20) if btn_menu_focus else (140, 140, 140)

        fenetre.blit(fond, (0, 0))
        #le titre
        fenetre.blit(titre, (fenetre.get_size()[0] // 2 - titre.get_size()[0] // 2, 3))
        #les sections
        for k in range(3):
            if k != 2:
                fenetre.blit(surf_noire,
                    ((fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k, 60))
            else:
                fenetre.blit(surf_noire2,
                    ((fenetre.get_size()[0] - 3 * (surf_noire2.get_size()[0] + 20)) // 2 + (surf_noire2.get_size()[0] + 20) * k, 60))
            if not k or k == 1:
                titre_section = grd_font.render('Commandes', 1, (10, 10, 10))
                fenetre.blit(titre_section, ((fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k - titre_section.get_size()[0] // 2 + surf_noire.get_size()[0] // 2, 60))
                if not k:
                    for l in range(0, 29):
                        fenetre.blit(grd_font.render(liste_commandes[l][:-1], 1, (10, 10, 10)), ((10 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k, 90 + l * 16))
                if k:
                    for m in range(29, len(liste_commandes)):
                        fenetre.blit(grd_font.render(liste_commandes[m][:-1], 1, (10, 10, 10)), ((10 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k, 90 + (m - 29) * 16))
            if k == 2:
                fenetre.blit(grd_font.render('Réglages du jeu', 1, (10, 10, 10)), ((240 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k, 60))
                for n in range(len(clikable)):
                    fenetre.blit(grd_font.render(clikable[n][0], 1, clikable[n][2]), ((10 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * k, 90 + 19 * n))

        pygame.draw.rect(fenetre, btn_menu_color, (btn_menu_pos[0], btn_menu_pos[1], largeur, hauteur))
        fenetre.blit(grd_font.render('Menu', 1, (10, 10, 10)), (btn_menu_pos[0] + 8, btn_menu_pos[1] + 11))

        #les events
        for e in pygame.event.get():
            if e.type == MOUSEBUTTONDOWN:
                if (10 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * 2 <= e.pos[0] <= (10 + fenetre.get_size()[0] - 3 * (surf_noire.get_size()[0] + 20)) // 2 + (surf_noire.get_size()[0] + 20) * 2 + surf_noire.get_size()[0] - 10:
                    if 0 <= (e.pos[1] - 90 - hauteur_fenetre) // 19 <= len(clikable) - 1:
                        fullscreen = clikable[(e.pos[1] - 90 - hauteur_fenetre) // 19][1](fenetre, grd_font, hauteur_fenetre, fullscreen)
                elif btn_menu_pos[0] <= e.pos[0] <= btn_menu_pos[0] + largeur and btn_menu_pos[1] + hauteur_fenetre <= e.pos[1] <= btn_menu_pos[1] + hauteur_fenetre + hauteur:
                    continuer = 0

        x_s, y_s = pygame.mouse.get_pos()
        if btn_menu_pos[0] <= x_s <= btn_menu_pos[0] + largeur and btn_menu_pos[1] + hauteur_fenetre <= y_s <= btn_menu_pos[1] + hauteur_fenetre + hauteur:
            btn_menu_focus = True
        else:
            btn_menu_focus = False

        pygame.display.flip()


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
                        jeu(hote, port, en_reseau, root_, fenetre, creatif_choisi, dossier_personnage, r.center)
                        #jeu(fenetre, "Guerrier", dossier_personnage, True, 500, 75, creatif_choisi, root_, r.center, r, largeur_dispo // 30 + 30, True, hote, port, realistic)
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
                        jeu(hote, port, en_reseau, root_, fenetre, creatif_choisi, dossier_personnage, r.center)
                        #jeu(fenetre, "Guerrier", dossier_personnage, True, 500, 75, creatif_choisi, root_, r.center, r, largeur_dispo // 30 + 30, en_reseau, hote, port, realistic)
                        pygame.mouse.set_visible(True)
                #bouton paramètres
                elif bouton_param[0] <= e.pos[0] <= bouton_param[0] + largeur * 4 \
                    and bouton_param[1] + hauteur_fenetre <= e.pos[1] <= bouton_param[1] + hauteur_fenetre + hauteur * 2:
                    parametres(fenetre, grd_font, hauteur_fenetre, fullscreen)
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