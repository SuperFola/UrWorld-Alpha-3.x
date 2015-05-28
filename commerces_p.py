# -*-coding: utf8-*

import pickle
import random
from BModules.reader import Reader
import constantes as cst
from BModules.discussion import *
import text_entry as txty


taille_sprite = 30
cote_fenetre = cst.cote_fenetre


def message_affiche_choix(message, rcenter):
    texte = Reader(message, pos=(rcenter[0] - 290, rcenter[1] + 210), width=cote_fenetre - 20, fontsize=16, height=80,
                   bg=(150, 150, 150), fgcolor=(20, 20, 20))
    # texte.TEXT = message
    continuer_2 = 1
    choix = "n"  # valeur par défaut
    while continuer_2:
        for event in pygame.event.get():
            texte.show()
            if event.type == JOYBUTTONUP:
                if event.button == 0:
                    choix = "o"
                    continuer_2 = 0
                elif event.button == 1:
                    choix = "n"
                    continuer_2 = 0
            elif event.type == KEYDOWN:
                if event.key == K_n:
                    choix = "n"
                    continuer_2 = 0
                elif event.key == K_o:
                    choix = "o"
                    continuer_2 = 0
            elif event.type != KEYDOWN and event.type != MOUSEBUTTONDOWN and event.type != JOYBUTTONUP:
                continue
            elif event.type == QUIT:
                sys.exit()
    return choix


def message_short(message, rcenter):
    # texte.TEXT = message
    texte = Reader(message, pos=(rcenter[0] - 290, rcenter[1] + 210), width=cote_fenetre - 20, fontsize=16, height=80,
                   bg=(150, 150, 150), fgcolor=(20, 20, 20))
    continuer_2 = 1
    tps_deb = time.time() + 2
    while continuer_2:
        pygame.time.Clock().tick(120)
        if time.time() >= tps_deb:
            continuer_2 = 0
        for event in pygame.event.get():
            texte.show()
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


def message_affiche_non_bloquant(message, rcenter):
    texte = Reader(message, pos=(rcenter[0] - 290, rcenter[1] + 210), width=cote_fenetre - 20, fontsize=16, height=80,
                   bg=(150, 150, 150), fgcolor=(20, 20, 20))
    # texte.TEXT = message
    texte.show()


def message_entre(surface, rcenter, font, arme_h_g):
    box = txty.TextEntry((rcenter[0] - 400 // 2 + 4, rcenter[1] - 28 // 2), surface, size=396)
    entrez_votre_txt = font.render('Entrez votre texte :', 1, (10, 10, 10))
    continuer = 1
    valide_btn = (rcenter[0] - 404 // 2 + 10, rcenter[1] + 75 - 20 - 10)
    x_s, y_s = (0, 0)

    while continuer:
        pygame.draw.rect(surface, (150, 150, 150), (rcenter[0] - 404 // 2, rcenter[1] - 150 // 2, 404, 150))
        surface.blit(entrez_votre_txt, (rcenter[0] - 404 // 2 - entrez_votre_txt.get_size()[0] // 2,
                                        rcenter[1] - 150 // 2 + 10))
        pygame.draw.rect(surface, (20, 180, 20), (valide_btn[0], valide_btn[1], 30, 20))

        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    continuer = 0
                else:
                    box.add_letter(e)
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    if valide_btn[0] <= x_s <= valide_btn[0] + 30 and \
                           valide_btn[1] <= y_s <= valide_btn[1] + 20:
                        continuer = 0
        box.render()
        x_s, y_s = pygame.mouse.get_pos()
        surface.blit(arme_h_g, (x_s, y_s))
        pygame.mouse.set_visible(False)
        pygame.display.flip()

    return box.value()


def message_affiche(message, rcenter):
    texte = Reader(message, pos=(rcenter[0] - 290, rcenter[1] + 210), width=cote_fenetre - 20, fontsize=16, height=80,
                   bg=(150, 150, 150), fgcolor=(20, 20, 20))
    # texte.TEXT = message
    continuer_2 = 1
    while continuer_2:
        pygame.time.Clock().tick(120)
        for event in pygame.event.get():
            texte.show()
            if event.type == KEYDOWN:
                continuer_2 = 0
            elif event.type == JOYBUTTONUP:
                continuer_2 = 0
            elif event.type != KEYDOWN and event.type != MOUSEBUTTONDOWN:
                continue
            elif event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


def message_affiche_large(message, fenetre, rcenter):
    texte = Reader(message, pos=(rcenter[0] - 290, rcenter[1] - 290), width=cote_fenetre + 200, fontsize=16, height=580,
                   bg=(150, 150, 150), fgcolor=(20, 20, 20))
    # texte.TEXT = message
    continuer_2 = 1
    while continuer_2:
        pygame.time.Clock().tick(120)
        pygame.draw.rect(fenetre, (10, 10, 10), (0, 0, 600, 600))
        for event in pygame.event.get():
            texte.show()
            if event.type == KEYDOWN:
                continuer_2 = 0
            elif event.type == JOYBUTTONUP:
                continuer_2 = 0
            elif event.type != KEYDOWN and event.type != MOUSEBUTTONDOWN and event.type != JOYBUTTONUP:
                continue
            elif event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


def vente(rcenter, fenetre, liste_prix, nom, blocs_, img_tous_blocs):
    pygame.font.init()
    font = pygame.font.Font("freesansbold.otf", 9)
    liste_blocs = [
        "q", "m", "t",
        "d", "e", "s",
        "h", "a", "r",
        "y", "u", "i",
        "M", "v", "l",
        "k", "g", "f",
        "x", "b", "n",
        "?", ".", "/"]
    monnaie_ajout = 0
    quantite = 0
    continuer = 1
    num_choix = 0
    choix_fait = False
    while continuer:
        pygame.time.Clock().tick(120)
        pygame.draw.rect(fenetre, (20, 20, 20), (10, 10, 580, 440))
        pygame.draw.rect(fenetre, (20, 180, 20), (290, 290, 19, 10))
        fenetre.blit(font.render("Valider", 1, (240, 240, 240)), (291, 291))
        fenetre.blit(
            font.render("Nombre de ventes : maximum (toutes les occurences du bloc seront vendus)", 1, (240, 240, 240)),
            (10, 585))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_F4:
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 5:  # la molette descend
                    if num_choix - 1 >= 0:
                        num_choix -= 1
                    elif num_choix == 0:
                        num_choix = len(nom)  # donc le dernier élément
                    else:
                        num_choix = 0
                elif event.button == 5:  # la molette monte
                    if num_choix + 1 > len(nom):
                        num_choix = 0
                    elif num_choix + 1 < len(nom):
                        num_choix += 1
                elif event.button == 1:  # clic gauche
                    if event.pos[0] >= 600 - 9 and event.pos[0] <= 600 - 9 + 19 \
                            and event.pos[1] >= 600 - 9 and event.pos[1] <= 600 - 9 + 10:
                        choix_fait = True
        if choix_fait:
            pygame.draw.rect(fenetre, (20, 180, 20), (400, 300 - 225, 16, 10))
            fenetre.blit(font.render(quantite, 1, (10, 10, 10)), (402, 300 + 2))
            pygame.display.flip()
            continuer = 0
        fenetre.blit(img_tous_blocs[liste_blocs[num_choix]], (34, 300))
        pygame.display.flip()

    monnaie_ajout = blocs_[liste_blocs[num_choix]]
    blocs_[liste_blocs[num_choix]] = 0

    with open("Parties" + os.sep + "bloc.sav", "wb+") as bloc_save:
        mon_pickler = pickle.Pickler(bloc_save)
        mon_pickler.dump(blocs_)
    return monnaie_ajout * liste_prix[liste_blocs[num_choix]]


def passant_parle(fenetre, situation_actuelle, personnage, structure, monnaie, rcenter, img_tous_blocs, fov):
    """
    Les personnages sont symbolisés par :
    1	2	3	4	5
    6	7	8	9	0
    *	-	+	/
    dans le code source des niveaux.
    fenetre : surface
    situation_actuelle : orientation du personnage
    x_perso : position en x du perso
    y_perso : position en y du perso
    structure : niveau en lui meme
    monnaie : quantité d'argent
    rcenter : centre de la zone de jeu
    img_tous_blocs : liste des images de tout les blocs
    fov : field of view
    """
    personne_a_parler = ""  # il faut la déterminer avec tout ce qui envoyé à la fonction
    dernier_x = personnage.get_pos()[0]
    dernier_y = personnage.get_pos()[1]
    case_x = personnage.get_pos()[0] // 30 + fov[0]
    case_y = personnage.get_pos()[1] // 30
    qui_perso = ['1', '2', '3', '4', '5', '6', '7', '8']

    if situation_actuelle == 'droite':
        if structure[case_y][case_x + 1] in qui_perso:
            # affectation d'un personnage
            personne_a_parler = structure[case_y][case_x + 1]

    if situation_actuelle == 'gauche':
        if structure[case_y][case_x - 1] in qui_perso:
            personne_a_parler = structure[case_y][case_x - 1]

    recupere_intercalere = cst.parole_passants
    if personne_a_parler in qui_perso:
        msg_parle = recupere_intercalere[personne_a_parler][0] + ' : ' + random.choice(recupere_intercalere[personne_a_parler][1])
        message_affiche(msg_parle, rcenter)
    else:
        message_affiche("A qui souhaites tu parler ?", rcenter)