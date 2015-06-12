"""Constantes du jeu UrWorld"""

import time
import os
from tkinter import *


def truncature(x, precision=2):
    new_x = str(x)[:precision+2]
    return float(new_x)


t = Tk()
taille_fenetre_largeur_win = t.winfo_screenwidth()
taille_fenetre_hauteur = t.winfo_screenheight()
t.destroy()

# Paramètres de la fenêtre
nombre_sprite_cote = 20
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite

#variables
structure = []
var_equipement = 3
int_cpt = 0
transparence = 250
monnaie = 5000
fps = 50
ok_joy = 0
continuer = 1
mode = 0
x = 0
y = 0
backsl_t = "\t\t\t"
dossier_personnage = "0" + os.sep
Choix = ""
trouvaille = ""
arme_personnage = ""
equipement_en_cours = ""
quoi = ""
pseudo = ""
pelle = True
eau_proche = False
blablabla_peche = False
tresors_trouve = False
choisi_un_avatar = False
a_tente_de_jouer = False
mode_de_jeu = False
pas_de_partie = True

valeur_transparence_eau = 156


cds = {
    'qs': None,
    'sd': None,
    'df': None,
    'fg': None
}

parole_passants = {
        "1": [
            "@Folaefolc",
                [
                    "Bonjour ! Je suis le créateur du jeu, je vous souhaite une bonne aventure tout comme l'a été pour moi la création de ce jeu !",
                    "Si tu as un problème, le site web est là pour toi !",
                    "Ne t'inquiètes pas,je ne mange pas !",
                    "Tu veux jouer avec moi ? J'adore construire de mes mains !",
                    "Je vois que ton aventure se poursuit sans encombres, je suis content pour toi.",
                    "Salut ! Que viens tu faire ici (n'ai pas peur je vais pas te crier dessus :) ) ?",
                    "Oh ! Regarde, des blocs ! Trop drôle, ma blague est nulle mais à chaque fois tu t'attend à quelque chose d'extraordinaire !",
                    "Hey ! Comment ça va toi ? Moi je vais bien, je continu d'améliorer ce chez d'oeuvre !"
                ]
            ],
    "2": [
        "Lynk",
            [
                "Bonjour ! Comment va tu ?",
                "Je me balade dans la forêt avec mes amis, moi le week-end.",
                "Fait attention à toi quand tu te balades !",
                "J'aime bien me cacher dans la forêt pour jouer avec mes amis !",
                "La vie, c'est génial, ce monde est génial, il ne te reste qu'à le rendre à ton image :) !",
                "Il y a peu de block disponnibles, mais beaucoup de possiblités de customisations !",
                "J'espère que cette aventure te plait, et que tu en ressortiras grandis d'une nouvelle expérience.",
                "Tu veux me défier ? J'aime bien te parler mais là je suis un peu fatigué !"
            ]
        ],
    "3": [
        "????",
            [
                "Salut ! Ca va ?",
                "La vie est belle, il serait bête de ne pas en profiter !",
                "Où suis-je ? Qui suis-je ? Quel est le but de la vie ? Je ne sais pas ...",
                "Je ne sais pas. Je te connais ? Mais oui ... ou non ?",
                "Excuse moi, mais je crois bien m'être perdu ...",
                "Bonjour, je ne sais pas ce que je fais ici ... j'ai atterit dans ce monde par hasard sans savoir comment ni pourquoi ...",
                "Ouh lala ... mais que faire ? Que faire ? Que faire ? Pourrais-tu m'aider ?",
                "Je ne cesse de me perdre, c'est assez horible ... J'erre sans but ni quête à la recherche de je-ne-sais-quoi ..."
            ]
        ],
    "4": [
        "Maryo",
            [
                "Bonjour ! Ce monde est . . . étrange. Je viens d'un autre endroit où les dragons nous courent après pour enlever nos princesses !",
                "Le côté \"poillu\" est sympa je trouve.",
                "Hello :D Aurais-tu par hasard vu ma petite amie ? Comment, tu ne la connais pas ?",
                "It's me, Maryo ! Moi et mon frère on adore se sauter sur la champignon !",
                "Si un jour tu croises un dragon, bon ou méchant, hésite pas et balance lui une tortue !",
                "En cas d'ennuie, tu m'appelles hein ? Je pourrais t'aider ;)"
            ]
        ],
    "5": [
        "Cédric",
            [
                "Hello ! I come from England. I would like to know why are we there ?",
                "Do you understand the english ? I am lost !",
                "Why this game is in french ?! Everybody know that the best games are english !",
                "Hey you ! Get out from my bloc !",
                "You don't speak english ? Ohhh no, I would never return in my country ...",
                "... Help ... I don't know this country, there isn't rain or snow ..."
            ]
        ],
    "6": [
        "Mineur",
            [
                "Salut toi ! Tu as une tête de nouveau ou c'est moi . . . ?",
                ". . . Que me veut tu ?",
                "Creuse, creuse et trouve. Casse, Casse et trouve ... Voilà, trouveée ! Ma précieuse ... ma belle pépite d'or !",
                "Ahhh, que j'aime être sous terre ! Quelle fraicheure peut on y trouver !",
                "Y aurait il quelqu'un pour me prêter une pelle ?",
                "Aïe aïe aïe, j'ai cassé ma pioche !! Comment vais je bien pouvoir continuer a creuser ?",
                "Bonjour toi, on se connait peut être ? Je t'aurais déjà vu sous terre ?",
                "Aurais tu des cailloux pour moi ? De l'or ? Du diamant ? Des rubis ?"
            ]
        ],
    "7": [
        "Nolwenn",
            [
                "Dans la vallée wo ho, de Danna . . . dalidali dada !",
                "J'aime la musique !",
                "Tu n'aurais un petit CD sur toi ? J'ai terminé toutes mes pistes audios et je m'ennuie un peu ...",
                "Tu as déjà utilisé un jukebox ? Non ? Prends un CD, et fait un clic droit sur un jukebox, cela jouera la musique du CD !",
                "La musique fait battre nos coeurs, et nous permet d'oublier nos soucis !",
                "Allez, dance avec moi !"
            ]
        ],
    "8": [
        "Spéléologue",
            [
                "Salut, marche à l'ombre ! (Laisse béton . . .)",
                "Ici se trouve des fossiles très rares qui pouraient même dater d'avant les dinosaures, celui-ci pourait même rennaître.",
                "Mon ami mineur a déniché des fossiles d'une rareté sans égale récemment ! Veut tu les voir ?",
                "Toi aussi tu pourrais creuser pour moi et m'amener les fossiles que tu trouverais ? Non ? Quel dommage ...",
                "Oh zût alors ! Voici bien un fossile de Cranatosaurus Tuliporus ! Qu'il est beau ... !",
                "Un musée de spéléologie devrait apparemment ouvrir dans les prochaines années ... Quel bonheur pour moi !",
                "Je suis chercheur de fossile, ou plutôt collectionneur.",
                "Je n'aime pas aller sous terre en fait, je préfère que d'autres se chargent de déterrer des fossiles pour moi, pendant que je les examine !",
                "Comme mes fossiles sont beaux non ?"
            ]
        ]
}


class IAFPS:
    def __init__(self, FPS):
          self.FPS = FPS / 10
          self.defaut_value = self.FPS
          self.reduction = 0.0005
          self.wait = 0.001

    def timer(self, frame_rate):
        self.frame_rate = frame_rate
        if self.frame_rate > self.FPS:
            self.wait += self.reduction
        elif self.frame_rate < self.FPS:
            self.wait -= self.reduction
            if self.wait <= 0:
                self.wait = 0
        #print("temps de pause (sec) :: " + str(self.wait))
        #print("frame_rate compté dans la boucle :: " + str(self.frame_rate))

    def pause(self):
        time.sleep(self.wait)

    def set_FPS(self, nv_FPS):
        self.FPS = nv_FPS / 10

    def default(self):
        self.FPS = self.defaut_value