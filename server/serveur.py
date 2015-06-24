# -*-coding: utf8-*

#import  win32com.client as com
from gentest import *
import platform as p
import subprocess
import socket
import pickle
import time
import sys
import re
import os
import glob
from math import ceil

class Inventory:
    def __init__(self):
        self.blocs = {}

    def get(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['quantity']
        return 0

    def use(self, item, nbr=1):
        if item in self.blocs.keys():
            self.blocs[item]['quantity'] -= nbr
            if self.blocs[item]['quantity'] < 0:
                self.blocs[item]['quantity'] = 0
                return False
            return True
        return None

    def set(self, item, nbr=1):
        if item in self.blocs.keys():
            self.blocs[item]['quantity'] = nbr
            return True
        return False

    def add(self, item, solid=True, shadow=0, gravity=False, quantity=0, innafichable=False, name='', tps_explode=0, take_fire=False):
        self.blocs[item] = {
            'solid': solid,
            'shadow': shadow,
            'gravity': gravity,
            'unprintable': innafichable,
            'quantity': quantity,
            'name': name,
            'destruction_time': tps_explode,
            'fireable': take_fire
        }

    def get_shadow(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['shadow']
        return 0

    def get_solid(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['solid']
        return True

    def get_gravity(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['gravity']
        return None

    def get_unprintable(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['unprintable']
        return False

    def get_fire(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['fireable']
        return False

    def get_time(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['destruction_time']
        return 0

    def list_solid(self):
        solid_lst = []
        for i in self.blocs:
            if self.blocs[i]['solid']:
                solid_lst.append(i)
        return solid_lst

    def list_gravity(self):
        gravity_lst = []
        for j in self.blocs:
            if self.blocs[j]['gravity']:
                gravity_lst.append(j)
        return gravity_lst

    def list_unprintable(self):
        unprintable_lst = []
        for k in self.blocs:
            if self.blocs[k]['unprintable']:
                unprintable_lst.append(k)
        return unprintable_lst

    def list_fire(self):
        fire_lst = []
        for l in self.blocs:
            if self.blocs[l]['fireable']:
                fire_lst.append(l)
        return fire_lst

    def list(self):
        lst = []
        for m in self.blocs:
            lst.append(m)
        return lst

    def dict_name(self):
        dico_name = {}
        for n in self.blocs:
            dico_name[n] = self.blocs[n]['name']
        return dico_name


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


try:
    result = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE).stdout.read()
    adresse_mac = re.search('([0-9A-F]{2}-?){6}', str(result)).group()
    adresse_mac = adresse_mac.split('-')
    adresse_mac = ':'.join(adresse_mac)
except NameError as nom_err:
    print(nom_err)
except TypeError as type_err:
    print(type_err)


def local_qui_est_tu():
    result = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE).stdout.read()
    adresse_mac = re.search('([0-9A-F]{2}-?){6}', str(result)).group()
    adresse_mac = adresse_mac.split('-')
    adresse_mac = ':'.join(adresse_mac)
    nom_de_session = os.getenv("USERNAME")
    cpu_corps = str(os.cpu_count())
    hote = socket.gethostbyname(socket.gethostname())
    drive = 'C:/'
    systeme = p.system()
    python = p.python_version()
    jeu, formatFichier = p.architecture()
    distribution = p.version()
    print("\t[*] " + "Système      Opérant     ::   " + systeme)
    print("\t[*] " + "Nombre Coeurs Processeur ::   " + cpu_corps, end='   ')
    print("-   Correct" if int(cpu_corps) >= 2 else "-   Insuffisant")
    print("\t[*] " + "Architecture Processeur  ::   " + jeu)
    print("\t[*] " + "Version      Système     ::   " + distribution)
    print("\t[*] " + "Version      Python      ::   " + python)
    print("\t[*] " + "Adresse      IP          ::   " + hote)
    print("\t[*] " + "Adresse      MAC         ::   " + adresse_mac)
    print("\t[*] " + "Session      Active      ::   " + nom_de_session)
    print("")


def map_generator():
    print('In[0] : Début de la génération ...')
    start = time.time()
    if not os.path.exists("map.lvl"):
        length, flatness, height = 4096, 4, 20
        headstart, deniv = height // 2, 1
        my_noise_ = list(Map(length, flatness, range(1, height), headstart, deniv))
        for y, ligne in enumerate(my_noise_):
            for x, elem in enumerate(ligne):
                my_noise_[y][x] = str(my_noise_[y][x])
        with open("map.lvl", "wb") as file:
            pickle.Pickler(file).dump(my_noise_)
    print('Out[1]: %2i minutes %2i secondes.' % (int((time.time() - start) // 60), int((time.time() - start) % 60)))
    print('In[0]: Fin de la génération !\n')


white_list = {}

#8 : banni
#16 : user
#32 : modo
#64 : admi
#128 : serveur

wl = {
    'colors':
    {
        8:  (0, 0, 0),
        16: (255, 255, 255),
        32: (20, 180, 20),
        64: (180, 20, 20)
    },
    'users':
    {
        'folaefolc': 64,
        'test': 16
    },
    'bannis':
    [
    ],
    'serveur_name': '',
    'serveur_description': '',
    'pvp': True,
    'secure': True
}

if os.path.exists("wl.txt"):
    with open("wl.txt", "r") as white_list:
        white_list = eval(white_list.read())
else:
    with open("wl.txt", "w") as wl_w:
        white_list = wl
        wl_w.write(white_list)
with open("serveur_data.txt", "r") as serv_carac:
    temp = serv_carac.read()
    white_list['serveur_name'] = temp.split(':')[0]
    white_list['serveur_description'] = temp.split(':')[1]


os.system("color 0f")
texte_serv_bienvenue = "***** " + white_list['serveur_name'] + ", bienvenue. *****\n\n\n"
print(" " * (78 // 2 - len(texte_serv_bienvenue) // 2) + texte_serv_bienvenue)

hote = ''
try:
    hote = socket.gethostbyname(socket.gethostname())
except NameError as nom_err:
    print(nom_err)
except TypeError as type_err:
    print(type_err)
print("\n" * 2 + " " * 21 + "Écoute sur le serveur {0}.\n".format(hote))

sport = 60000
while 1:
    sport = input(" " * 21 + "Entrez le port [60000] > ")
    print("\n")
    if sport.strip() == "":
        sport = 60000
        break
    try:
        sport = sport.strip()
        int(sport)
        break
    except ValueError:
        print("Out[1]: Dis Toto, t'as pas compris ? Il me faut un chiffre !\n")

print("_" * 77 + "\n" + "|/-\\" * (79 // 4) + "\n" + "|   " * (79 // 4))

port = int(sport)
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connexion_principale.bind((hote, port))
print("\nIn[0]: Le serveur écoute à présent sur le port {0} depuis {1}.\n".format(port, hote))

local_qui_est_tu()
print("")

serveur_lance = True
to_print = input("Entrez 0 pour enregistrer les I/O dans un fichier, ou\n1 pour les afficher (peut faire ralentir le jeu)\n> ")
while to_print not in ['0', '1']:
    to_print = input("Entrez 0 pour enregistrer les I/O dans un fichier, ou\n1 pour les afficher (peut faire ralentir le jeu)\n> ")
to_print = bool(int(to_print))
to_save_into_file = ""
BUFFER_SIZE = 4096
connectes = {}
msg_chat = []
carte = []
if not os.path.exists('map.lvl'):
    map_generator()
with open("map.lvl", 'rb') as f:
    carte = pickle.Unpickler(f).load()
pancartes_txt = []
teleporteurs_addr = []
if os.path.exists('teleporteurs.sav'):
    with open('teleporteurs.sav', 'rb') as telep_r:
        teleporteurs_addr = pickle.Unpickler(telep_r).load()

print("L'affichage I/O est activé" if to_print else "L'affichage I/O se fera dans un fichier")

while serveur_lance:
    data, addr = connexion_principale.recvfrom(BUFFER_SIZE)
    if addr not in connectes.keys():
        datas = pickle.loads(data)
        datas = {
            #simplement le pseudo
            'pseudo': datas[0],
            #en cases avec le fov préintégré dedans
            'x': datas[1],
            #en cases aussi
            'y': datas[2],
            #le FOV actif
            'fov': [0, 75],
            #la direction du personnage
            'dir': 1,
            #juste le dossier, pas l'image
            'repr': datas[3],
            #le message qu'il faudra afficher
            'cur_msg': '',
            #la couleur dans laquelle sera le pseudo
            'color': (255, 255, 255),
            #la vie du personnage
            'vie': 100
        }
        connectes[addr] = datas
        #on dit au client si le serveur est sécurisé ou non
        connexion_principale.sendto(pickle.dumps(white_list['secure']), addr)
        if white_list['secure']:
            #il faut un mot de passe pour se connecter au serveur !
            mot_de_passe_client, addr2 = connexion_principale.recvfrom(BUFFER_SIZE)
            mot_de_passe_client = pickle.loads(mot_de_passe_client)
            if connectes[addr]['pseudo'] in white_list['authentification']:
                if white_list['authentification'][connectes[addr]['pseudo']] == mot_de_passe_client:
                    connexion_principale.sendto(pickle.dumps(True), addr)
                else:
                    connexion_principale.sendto(pickle.dumps(False), addr)
            else:
                connexion_principale.sendto(pickle.dumps(False), addr)
        if connectes[addr]['pseudo'] in white_list['users'].keys():
            grade = white_list['users'][connectes[addr]['pseudo']]
            couleur = white_list['colors'][grade]
            connectes[addr]['color'] = couleur
            print("In[0]: Nouveau client : '%s' #%i" % (connectes[addr]['pseudo'], grade))
        else:
            print("In[0]: Nouveau client : '%s'" % connectes[addr]['pseudo'])

    if data:
        data = pickle.loads(data)
        if to_print:
            print("In[0]: Le client '%s' envoit %s" % (connectes[addr]['pseudo'], str(data)))
        else:
            to_save_into_file += "in : %s envoit %s" % (str(connectes[addr]['pseudo']), str(data))
            to_save_into_file += "\n"
        if type(data) == str:
            if data[:5] == 'get->' and data[5:9] != 'chat' and data[5:] != "configuration" and data[5:] != 'others' \
                    and data[5:10] != 'telep' and data[5:8] != 'pan'and data[5:] != 'life':
                #demande d'un bloc en particulier
                coor = data[5::]
                coor = coor.split(':')
                if to_print:
                    print("In[0]: %s veut connaitre le bloc en [%i, %i](%s)" % (connectes[addr]['pseudo'], int(coor[0]), int(coor[1]), carte[int(coor[1])][int(coor[0])]))
                else:
                    to_save_into_file += 'in : %s veut le bloc %i %i %s' % (connectes[addr]['pseudo'], int(coor[0]), int(coor[1]), carte[int(coor[1])][int(coor[0])])
                    to_save_into_file += "\n"
                connexion_principale.sendto(pickle.dumps(carte[int(coor[1])][int(coor[0])]), addr)
                if to_print:
                    print("Out[1]: tile [%i, %i](%s) envoyé à %s" % (int(coor[0]), int(coor[1]), carte[int(coor[1])][int(coor[0])], connectes[addr]['pseudo']))
                else:
                    to_save_into_file += 'out : envoie du tile demandé à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data[:10] == 'get->telep':
                #on veut utiliser un téléporteur
                depart = data[10:].split(',')
                x = int(depart[0])
                y = int(depart[1])
                dedans = False
                if to_print:
                    print("In[0]: %s veut utiliser le téléporteur placé en (%i, %i)" % (connectes[addr]['pseudo'], x, y))
                else:
                    to_save_into_file += 'in : %s utilise le teleporteur en %i %i' % (connectes[addr]['pseudo'], x, y)
                    to_save_into_file += "\n"
                for i in range(len(teleporteurs_addr)):
                    if teleporteurs_addr[i][0] == (x, y):
                        connexion_principale.sendto(pickle.dumps(teleporteurs_addr[i][1]), addr)
                        dedans = True
                        if to_print:
                            if teleporteurs_addr[i][1] != '':
                                go_x, go_y = teleporteurs_addr[i][1]
                                go_x -= connectes[addr]['fov'][0]
                            else:
                                go_x, go_y = 'Erreur', 'Erreur'
                            print("Out[1]: envoit des coordonnées d'arrivée (%i, %i) à %s" % (go_x, go_y, connectes[addr]['pseudo']))
                        else:
                            to_save_into_file += 'out : envoit des coordonnées d\' arrivée à %s' % connectes[addr]['pseudo']
                            to_save_into_file += "\n"
                        break
                    elif teleporteurs_addr[i][1] == (x, y):
                        connexion_principale.sendto(pickle.dumps(teleporteurs_addr[i][0]), addr)
                        dedans = True
                        if to_print:
                            if teleporteurs_addr[i][1] != '':
                                go_x, go_y = teleporteurs_addr[i][0]
                                go_x -= connectes[addr]['fov'][0]
                            else:
                                go_x, go_y = 'Erreur', 'Erreur'
                            print("Out[1]: envoit des coordonnées d'arrivée (%i, %i) à %s" % (go_x, go_y, connectes[addr]['pseudo']))
                        else:
                            to_save_into_file += 'out : envoie des coordonées d\'arrivée à %s' % connectes[addr]['pseudo']
                            to_save_into_file += "\n"
                        break
                if not dedans:
                    connexion_principale.sendto(pickle.dumps((x, y)), addr)
            elif data == 'get->life':
                #on veut connaitre notre vie
                if to_print:
                    print('In[0]: %s veut connaitre sa vie' % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s veut connaitre sa vie' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                connexion_principale.sendto(pickle.dumps(connectes[addr]['vie']), addr)
                if to_print:
                    print('Out[1]: %s recoit la valeur de sa vie %i' % (connectes[addr]['pseudo'], connectes[addr]['vie']))
                else:
                    to_save_into_file += 'out : %s recoit la valeur de sa vie %i' % (connectes[addr]['pseudo'], connectes[addr]['vie'])
                    to_save_into_file += "\n"
            elif data[:9] == 'set->life':
                #on veut changer la valeur de notre vie
                quantity = ceil(float(data[9:]))
                connectes[addr]['vie'] += quantity
                if connectes[addr]['vie'] > 100:
                    connectes[addr]['vie'] = 100
            elif data[:8] == 'get->pan':
                #on veut les infos d'un panneau
                if to_print:
                    print("In[0]: %s veut connaitre le texte d'une pancarte !" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s lit une pancarte' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                pancarte_pos = data[8:].split(',')
                to_send = pickle.dumps('')
                for i in range(len(pancartes_txt)):
                    if pancartes_txt[i][0] == (int(pancarte_pos[0]), int(pancarte_pos[1])):
                        to_send = pickle.dumps(pancartes_txt[i][1])
                        break
                connexion_principale.sendto(to_send, addr)
                if to_print:
                    print("Out[1]: envoie du texte de la pancarte à %s" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'out : envoit du texte à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data[:10] == "break->pan":
                #on veut casser une pancarte
                if to_print:
                    print("In[0]: %s a cassé une pancarte" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s a cassé une pancarte' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                pos_pan = data[10:].split(',')
                for i in range(len(pancartes_txt)):
                    if pancartes_txt[i][0] == (int(pos_pan[0]), int(pos_pan[1])):
                        pancartes_txt.pop(i)
                        break
            elif data[:8] == 'set->pan':
                #on veut poser une pancarte
                if to_print:
                    print("In[0]: %s a posé|modifié une pancarte" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s a posé|modifié une pancarte' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                pancartes_opt = data[8:].split(',')
                if len(pancartes_opt) == 3:
                    for i in range(len(pancartes_txt)):
                        if pancartes_txt[i][0] == (int(pancartes_opt[0]), int(pancartes_opt[1])):
                            pancartes_txt[i][1] = pancartes_opt[2]
                            break
                else:
                    pancartes_txt.append([(int(pancartes_opt[0]), int(pancartes_opt[1])), ''])
            elif data[:10] == 'set->telep':
                #on pose un téléporteur
                new_telep = data[10:].split(',')
                x_new = int(new_telep[0])
                y_new = int(new_telep[1])
                if teleporteurs_addr:
                    if teleporteurs_addr[len(teleporteurs_addr) - 1][1] == '':
                        teleporteurs_addr[len(teleporteurs_addr) - 1][1] = (x_new, y_new)
                    elif teleporteurs_addr[len(teleporteurs_addr) - 1][1] != '':
                        teleporteurs_addr.append([(x_new, y_new), ''])
                else:
                    teleporteurs_addr.append([(x_new, y_new), ''])
            elif data == "get->configuration":
                #on veut connaitre le nom et la description du serveur !
                if to_print:
                    print("In[0]: %s souhaite connaitre le nom et la description du serveur" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s demande les details du serveur' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                connexion_principale.sendto(pickle.dumps([white_list['serveur_name'], white_list['serveur_description']]), addr)
                if to_print:
                    print("Out[1]: envoie du nom et de la description du serveur à %s" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'out : envoit des détails à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data == "get->chat":
                if to_print:
                    print("In[0]: %s veut obtenir les messages du chat" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s demande les messages du chat' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                connexion_principale.sendto(pickle.dumps(msg_chat[:6]), addr)
                if to_print:
                    print("Out[1]: messages du chat envoyés à %s" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'out : envoie des messages à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data == "get->others":
                #on veut savoir si il y a d'autres personnes dans notre FOV
                if to_print:
                    print("In[0]: %s veut savoir s'il y a d'autres joueurs dans son champ de vision" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s veut savoir si il y a d\'autres joueurs proches' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                visibles = []
                for k, v in connectes.items():
                    if k != addr:
                        #on ne se traite pas soi même
                        if connectes[addr]['fov'][0] <= connectes[k]['x'] <= connectes[addr]['fov'][1]:
                            visibles.append([connectes[k]['x'], connectes[k]['y'], connectes[k]['pseudo'],
                                             connectes[k]['repr'], connectes[k]['dir'], connectes[k]['color']])
                connexion_principale.sendto(pickle.dumps(visibles), addr)
                if to_print:
                    print("Out[1]: envoie des positions, représentations, et pseudos des personnes visibles par %s à %s" % (connectes[addr]['pseudo'], connectes[addr]['pseudo']))
                else:
                    to_save_into_file += 'out : envoie des personnes visible à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data[:8] == 'set->pos':
                #un joueur renseigne sa position
                temp = data[8::]
                temp = temp.split(':')
                connectes[addr]['x'] = int(temp[0])
                connectes[addr]['y'] = int(temp[1])
                connectes[addr]['dir'] = 1 if temp[2] == 'droite' else -1
                if to_print:
                    print("In[0]: %s renseigne sa position (%s, %s) au serveur" % (connectes[addr]['pseudo'], temp[0], temp[1]))
                else:
                    to_save_into_file += 'in : position de %s : %s %s' % (connectes[addr]['pseudo'], temp[0], temp[1])
                    to_save_into_file += "\n"
                if to_print:
                    print("Out[1]: la position de %s a bien été enregistrée" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'out : position de %s enregistrée' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data[:9] == 'set->chat':
                if connectes[addr]['pseudo'] not in white_list['bannis']:
                    message = data[9::]
                    message = connectes[addr]['pseudo'] + ' : ' + message
                    msg_chat.insert(0, [message, connectes[addr]['color']])
                    if to_print:
                        print("In[0]: %s a envoyé le message %s dans le chat" % (connectes[addr]['pseudo'], message))
                        print("Out[1]: le message de %s a été ajouté au chat" % connectes[addr]['pseudo'])
                    else:
                        to_save_into_file += 'in : %s envoit le message %s' % (connectes[addr]['pseudo'], message)
                        to_save_into_file += "\n"
                        to_save_into_file += 'out : enregistrement du message de %s' % connectes[addr]['pseudo']
                        to_save_into_file += "\n"
            elif data[:5] == 'set->' and data[5:9] != 'chat' and data[5:8] != 'pos' and data[5:10] != 'telep' \
                    and data[5:8] != 'pan' and data[5:9] != 'life':
                #cassage de bloc
                if connectes[addr]['pseudo'] not in white_list['bannis']:
                    coor = data[5::]
                    coor = coor.split(':')
                    if to_print:
                        print("In[0]: %s a cassé un bloc en x: %i, y: %i pour mettre : %s" % (connectes[addr]['pseudo'], int(coor[0]), int(coor[1]), coor[2]))
                    else:
                        to_save_into_file += 'in : %s met %s en %i %i' % (connectes[addr]['pseudo'], coor[2], int(coor[0]), int(coor[1]))
                        to_save_into_file += "\n"
                    for i in connectes.keys():
                        if int(coor[0]) != connectes[i]['x'] + connectes[i]['fov'][0] and int(coor[1]) != connectes[i]['y']:
                            #on pose le bloc, il n'y a personne
                            carte[int(coor[1])][int(coor[0])] = coor[2]
                        else:
                            if white_list['pvp']:
                                #on pete la gueule à l'autre !
                                #donc on va devoir stocker la vie de tous les joueurs et ils devront la demander :)
                                for j in connectes.keys():
                                    if connectes[j]['x'] == int(coor[0]) and connectes[j]['y'] == int(coor[1]):
                                        connectes[j]['vie'] -= blocs.get_time(coor[2])
                                        if connectes[j]['vie'] <= 0:
                                            connectes[j]['vie'] = 0
                            else:
                                #pas de pvp, on ne fait rien
                                pass
                    if to_print:
                        print("Out[1]: cassage du bloc[%i, %i](%s) par %s défini dans la carte locale" % (int(coor[0]), int(coor[1]), coor[2], connectes[addr]['pseudo']))
                    else:
                        to_save_into_file += 'out : cassage du bloc %i %i' % (int(coor[0]), int(coor[1]))
                        to_save_into_file += "\n"
                else:
                    if to_print:
                        print("Out[1]: %s est banni et ne peut donc pas poser de bloc" % connectes[addr]['pseudo'])
                    else:
                        to_save_into_file += 'out : %s est banni et ne peut pas agir' % connectes[addr]['pseudo']
                        to_save_into_file += "\n"
            elif data[:5] == 'map->':
                #demande d'une partie de la map
                fov_to_send = data[5::]
                fov_to_send = fov_to_send.split(':')
                connectes[addr]['fov'] = [int(fov_to_send[0]), int(fov_to_send[1])]
                if to_print:
                    print("In[0]: %s veut connaitre la map en [%i, %i]" % (connectes[addr]['pseudo'], int(fov_to_send[0]), int(fov_to_send[1])))
                else:
                    to_save_into_file += 'in : %s demande la map en %i %i' % (connectes[addr]['pseudo'], int(fov_to_send[0]), int(fov_to_send[1]))
                    to_save_into_file += "\n"
                connexion_principale.sendto(pickle.dumps([line[int(fov_to_send[0]):int(fov_to_send[1]):] for line in carte]), addr)
                if to_print:
                    print("Out[1]: map [%i -> %i] envoyé à %s" % (int(fov_to_send[0]), int(fov_to_send[1]), connectes[addr]['pseudo']))
                else:
                    to_save_into_file += 'out : envoie de la map à %s' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
            elif data == "save":
                #demande de sauvegarde de la carte de la part d'un client
                if to_print:
                    print("In[0]: %s a demandé à sauvegarder la carte" % connectes[addr]['pseudo'])
                else:
                    to_save_into_file += 'in : %s sauvegarde' % connectes[addr]['pseudo']
                    to_save_into_file += "\n"
                with open("map.lvl", "wb") as save_serveur_map:
                    pickle.Pickler(save_serveur_map).dump(carte)
                    if to_print:
                        print("Out[1]: la carte a bien été sauvegardée")
                    else:
                        to_save_into_file += 'out : sauvegarde réussie'
                        to_save_into_file += "\n"
                with open("teleporteurs.sav", "wb") as telep_w:
                    pickle.Pickler(telep_w).dump(teleporteurs_addr)
                #del connectes[addr]  # on enleve le joueur du dico des connectes :D
            elif data[:5] == "ban->":
                #demande de ban d'un utilisateur
                a_bannir = data[5::]
                if to_print:
                    print("In[0]: quelqu'un souhaite bannir %s" % a_bannir)
                else:
                    to_save_into_file += 'in : %s va etre banni' % a_bannir
                    to_save_into_file += "\n"
                cur_grade = white_list['users'][connectes[addr]['pseudo']]
                if a_bannir in white_list['users'].keys():
                    grade_banni = white_list['users'][a_bannir]
                    if cur_grade > grade_banni:
                        white_list['bannis'].append(a_bannir)
                        if to_print:
                            print("Out[1]: %s a bien été banni" % a_bannir)
                    else:
                        if to_print:
                            print("Out[1]: le grade n'est pas assez important pour bannir %s" % a_bannir)
                else:
                    if to_print:
                        print("Out[1]: l'utilisateur %s n'existe pas" % a_bannir)
            elif data[:9] == "upgrade->":
                #on souhaite promouvoir un membre
                a_promouvoir = data[9::].split(',')[0]
                grade_donne = int(data[9::].split(',')[1])
                if to_print:
                    print("In[0]: %s va être promu par %s" % (a_promouvoir, connectes[addr]['pseudo']))
                else:
                    to_save_into_file += 'in : %s va etre promu' % a_promouvoir
                    to_save_into_file += "\n"
                cur_grade = white_list['users'][connectes[addr]['pseudo']]
                if a_promouvoir in white_list['users'].keys():
                    grade_promu = white_list['users'][a_promouvoir]
                    if cur_grade > grade_promu and cur_grade >= grade_donne:
                        white_list['users'][a_promouvoir] = grade_donne
                        if to_print:
                            print("Out[1]: %s a été promu par %s" % (a_promouvoir, connectes[addr]['pseudo']))
                    else:
                        if to_print:
                            print("Out[1]: le grade n'est pas suffisant pour cette opération")
                else:
                    if to_print:
                        print("Out[1]: l'utilisateur %s n'existe pas" % a_promouvoir)
    else:
        pass

if not to_print:
    with open('log_' + str(len(glob.glob("*.log")) + 1) + ".log", "w") as f:
        f.write(to_save_into_file)

input("Fermeture des connexions. Appuyez sur 'Entrée' pour quitter . . .")