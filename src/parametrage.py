import pygame
from pygame.locals import *
import dialog_box as dlb
import os
import random
import pickle
import re
import constantes as cst


largeur_dispo = cst.taille_fenetre_largeur_win


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
            with open(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "Settings" + os.sep + "couleur.sav", 'w') as clw:
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


def mode_gamer_switch(fenetre, grd_font, hauteur_fen, fullscreen):
    if os.path.exists(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamer.gm'):
        os.remove(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamer.gm')
        dlb.DialogBox(fenetre, ["Vous avez quitté le mode", "gamer"], "Style des controles",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
    else:
        dlb.DialogBox(fenetre, ["Vous êtes désormais un", "gamer !"], "Style des controles",
                                (fenetre.get_size()[0] // 2, fenetre.get_size()[1] // 2), grd_font, hauteur_fen,
                                type_btn=0, mouse=False).render()
        with open(".." + os.sep + "assets" + os.sep + 'Save' + os.sep + 'gamer.gm', 'w') as f:
            f.write('')
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


def parametres(fenetre, grd_font, hauteur_fenetre, fullscreen, in_game=False):
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
    mode_color = (15, 15, 170)
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
        ['Mode Gamer', mode_gamer_switch, mode_color],
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
        if not in_game:
            fenetre.blit(grd_font.render('Menu', 1, (10, 10, 10)), (btn_menu_pos[0] + 8, btn_menu_pos[1] + 11))
        else:
            fenetre.blit(grd_font.render('Jeu', 1, (10, 10, 10)), (btn_menu_pos[0] + 13, btn_menu_pos[1] + 11))

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
    fenetre.blit(pygame.image.load(".." + os.sep + "assets" + os.sep + "Menu" + os.sep + "Fond" + os.sep + "biome_foret.png").convert(), (-500, -900))