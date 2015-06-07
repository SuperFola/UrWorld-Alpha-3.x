# -*-coding: utf8-*

from commerces_p import *
from math import *
from ombrage_bloc import *
import glob
from weather import Weather
import pickle
import compressor as rle

pygame.display.init()
autre = pygame.display.set_mode((0, 0))

#police
font = pygame.font.Font("freesansbold.otf", 8)
font2 = pygame.font.Font("freesansbold.otf", 10)

img_ = {
    "q": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "bibli_thumbnail.png").convert_alpha(),
    "m": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "planche_thumbnail.png").convert_alpha(),
    "t": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "toit_thumbnail.png").convert_alpha(),
    "d": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "sable_thumbnail.png").convert_alpha(),
    "e": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "eau_thumbnail.png").convert_alpha(),
    "s": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "pierre_thumbnail.png").convert_alpha(),
    "h": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "herbe_thumbnail.png").convert_alpha(),
    "a": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "mine_or_thumbnail.png").convert_alpha(),
    "r": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "mine_charbon_thumbnail.png").convert_alpha(),
    "y": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "mine_diamant_thumbnail.png").convert_alpha(),
    "u": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "mine_emeraude_thumbnail.png").convert_alpha(),
    "i": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "mine_rubis_thumbnail.png").convert_alpha(),
    "M": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "demi_dalle_pierre_thumbnail.png").convert_alpha(),
    "v": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "verre_thumbnail.png").convert_alpha(),
    "l": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "verre_bleu_thumbnail.png").convert_alpha(),
    "k": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "verre_jaune_thumbnail.png").convert_alpha(),
    "g": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "verre_vert_thumbnail.png").convert_alpha(),
    "f": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "verre_rouge_thumbnail.png").convert_alpha(),
    "x": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "brique_thumbnail.png").convert_alpha(),
    "b": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "planche_sombre_thumbnail.png").convert_alpha(),
    "n": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "planche_claire_thumbnail.png").convert_alpha(),
    "?": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "demi_dalle_bois_thumbnail.png").convert_alpha(),
    ".": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "demi_dalle_bois_sombre_thumbnail.png").convert_alpha(),
    "/": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "demi_dalle_bois_clair_thumbnail.png").convert_alpha(),
    "p": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "indes_thumbnail.png").convert_alpha(),
    "A": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_bleue_thumbnail.png").convert_alpha(),
    "Z": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_gris_thumbnail.png").convert_alpha(),
    "E": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_jaune_thumbnail.png").convert_alpha(),
    "R": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_rose_thumbnail.png").convert_alpha(),
    "T": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_vert_thumbnail.png").convert_alpha(),
    "Y": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "laine_violet_thumbnail.png").convert_alpha(),
    "U": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "dirt_thumbnail.png").convert_alpha(),
    "I": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "neige_thumbnail.png").convert_alpha(),
    "O": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "tronc_thumbnail.png").convert_alpha(),
    "P": pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "feuille_thumbnail.png").convert_alpha(),
    'W': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "torche_bleu_thumbnail.png").convert_alpha(),
    'X': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "torche_vert_thumbnail.png").convert_alpha(),
    'C': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "torche_jaune_thumbnail.png").convert_alpha(),
    'V': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "torche_rouge_thumbnail.png").convert_alpha(),
    'B': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "jukebox_thumbnail.png").convert_alpha(),
    'az': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "champi_blanc_thumbnail.png").convert_alpha(),
    'ze': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "champi_rouge_thumbnail.png").convert_alpha(),
    'er': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "charbon_thumbnail.png").convert_alpha(),
    'rt': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "diamand_thumbnail.png").convert_alpha(),
    'ty': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "emeraude_thumbnail.png").convert_alpha(),
    'yu': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "or_thumbnail.png").convert_alpha(),
    'ui': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "rubis_thumbnail.png").convert_alpha(),
    'io': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "fleur_bleu_thumbnail.png").convert_alpha(),
    'op': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "fleur_rouge_thumbnail.png").convert_alpha(),
    'pq': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "fleur_jaune_thumbnail.png").convert_alpha(),
    'gh': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_bleu_thumbnail.png").convert_alpha(),
    'hj': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_gris_thumbnail.png").convert_alpha(),
    'jk': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_jaune_thumbnail.png").convert_alpha(),
    'kl': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_marron_thumbnail.png").convert_alpha(),
    'lm': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_marronc_thumbnail.png").convert_alpha(),
    'mw': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_marronf_thumbnail.png").convert_alpha(),
    'wx': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_rouge_thumbnail.png").convert_alpha(),
    'xc': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "table_vert_thumbnail.png").convert_alpha(),
    'c': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "commercant_thumbnail.png").convert_alpha(),
    'cv': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "nucleaire_thumbnail.png").convert_alpha(),
    'vb': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "telepo_thumbnail.png").convert_alpha(),
    'bn': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "pierre_eau_thumbnail.png").convert_alpha(),
    'n?': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "pierre_feu_thumbnail.png").convert_alpha(),
    '?.': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "pierre_terre_thumbnail.png").convert_alpha(),
    './': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "echelle_thumbnail.png").convert_alpha(),
    '%a': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "pancarte_thumbnail.png").convert_alpha(),
    '%b': pygame.image.load("Fond" + os.sep + "thumbnail" + os.sep + "time_telep_thumbnail.png").convert_alpha()
}

def souris_ou_t_es(fenetre, arme_h_g):
    x_souris, y_souris = pygame.mouse.get_pos()
    fenetre.blit(arme_h_g, (x_souris, y_souris))
    pygame.mouse.set_visible(False)
    return (x_souris, y_souris)


def fps_stp(temps_avant_fps, root, rcenter, font):
    """
    fonction pour afficher le nombre de FPS à l'ecran
    temps_avant_fps : dernier temps enregistré, servant à faire les calculs
    root : surface
    rcenter : centre du la zone de jeu
    font : police
    """
    #donc pas de division par zéro :P
    vrais_fps = trunc(((1000 / (time.time() - temps_avant_fps)) / 1000) if time.time() - temps_avant_fps else 300)
    #Titre avec les fps
    titre = "/* FPS : %5i */" % vrais_fps
    pygame.draw.rect(root, (75, 155, 180), (0, rcenter[1] + 360, 115, 20))
    root.blit(font.render(titre, 1, (10, 10, 10)), (4, rcenter[1] + 362))
    pygame.display.flip()


class Blocks:
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

    def get_name(self, item):
        if item in self.blocs.keys():
            return self.blocs[item]['name']
        return 'None'

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

class Carte:
    def __init__(self, surface, surface_mere, marteau, nb_blocs_large, blocs, rain=Weather(), storm=Weather(), wind=Weather()):
        self.ecran = surface
        self.root = surface_mere
        self.carte = None
        self.blocs = blocs
        self.marteau = marteau
        self.adresse = ""
        self.couleur_fond = (0, 184, 169)
        self.current_shader = "nul"
        self.compteur_shader = 0
        self.liste_shader = [
            'standart',
            'raycasté',
            'progressif',
            'gaussien',
            'nul'
        ]
        self.collision_bloc = self.blocs.list_solid()
        self.texture_pack = "Fond/"
        self.bloc_name = self.blocs.dict_name()
        self.y_max = 20
        self.x_max = 4096
        self.nb_blocs_large = nb_blocs_large
        self.fov = [0, self.nb_blocs_large]
        self.new_bloc = False
        self.gravity_entity = self.blocs.list_gravity()
        self.rain = rain
        self.storm = storm
        self.wind = wind
        self.start_fireing = -1
        self.bloc_fired = -1, -1
        self.map_surf = None
        self.last_map_lst = []

    def blocs_action(self, methode):
        self.blocs.methode()

    def load(self, adresse):
        self.adresse = adresse
        with open(adresse, 'rb') as map_reading:
            #self.carte = rle.RLEUncompress(map_reading).load()
            self.carte = pickle.Unpickler(map_reading).load()
            #self.carte = rle.load(map_reading)

    def load_image(self):
        # Chargement des images (seule celle d'arrivée contient de la transparence)
        #mode 'nuit'
        self.selection_bloc = pygame.image.load(self.texture_pack + "bleu_nuit.png").convert()
        self.bleu_nuit_1 = pygame.image.load(self.texture_pack + "bleu_nuit.png").convert_alpha()
        self.bleu_nuit_1.set_alpha(65)
        self.bleu_nuit_1.convert_alpha()
        self.bleu_nuit_2 = pygame.image.load(self.texture_pack + "bleu_nuit.png").convert()
        #blocs -----------------------------------------------------------------------------------------------
        #minerai
        self.mine_or = pygame.image.load(self.texture_pack + "mine_or.png").convert()
        self.mine_c = pygame.image.load(self.texture_pack + "mine_charbon.png").convert()
        self.mine_e = pygame.image.load(self.texture_pack + "mine_emeraude.png").convert()
        self.mine_d = pygame.image.load(self.texture_pack + "mine_diamant.png").convert()
        self.mine_r = pygame.image.load(self.texture_pack + "mine_rubis.png").convert()
        self.sol = pygame.image.load(self.texture_pack + "pierre.png").convert()
        self.demi_sol = pygame.image.load(self.texture_pack + "demi_dalle_pierre.png").convert_alpha()
        #complexes
        self.bibli = pygame.image.load(self.texture_pack + "bibli.png").convert()
        self.toit = pygame.image.load(self.texture_pack + "toit.png").convert()
        self.indes = pygame.image.load(self.texture_pack + "indes.png").convert()
        self.verre = pygame.image.load(self.texture_pack + "verre.png").convert_alpha()
        self.verre_b = pygame.image.load(self.texture_pack + "verre_bleu.png").convert_alpha()
        self.verre_j = pygame.image.load(self.texture_pack + "verre_jaune.png").convert_alpha()
        self.verre_v = pygame.image.load(self.texture_pack + "verre_vert.png").convert_alpha()
        self.verre_r = pygame.image.load(self.texture_pack + "verre_rouge.png").convert_alpha()
        self.briques = pygame.image.load(self.texture_pack + "brique.png").convert()
        #bois
        self.mur = pygame.image.load(self.texture_pack + "planche.png").convert()
        self.mur2 = pygame.image.load(self.texture_pack + "planche_sombre.png").convert()
        self.mur3 = pygame.image.load(self.texture_pack + "planche_claire.png").convert()
        self.demi_mur = pygame.image.load(self.texture_pack + "demi_dalle_bois.png").convert_alpha()
        self.demi_mur2 = pygame.image.load(self.texture_pack + "demi_dalle_bois_sombre.png").convert_alpha()
        self.demi_mur3 = pygame.image.load(self.texture_pack + "demi_dalle_bois_clair.png").convert_alpha()
        #aquatique
        self.sable = pygame.image.load(self.texture_pack + "sable.png").convert()
        self.eau_ = pygame.image.load(self.texture_pack + "eau.png").convert()
        self.eau_.set_alpha(cst.valeur_transparence_eau)
        pygame.Surface.convert_alpha(self.eau_)
        #naturels
        self.herbe = pygame.image.load(self.texture_pack + "herbe.png").convert()
        self.dirt = pygame.image.load(self.texture_pack + "dirt.png").convert()
        self.neige = pygame.image.load(self.texture_pack + "neige.png").convert()
        self.tronc = pygame.image.load(self.texture_pack + "tronc.png").convert()
        self.feuille = pygame.image.load(self.texture_pack + "feuille.png").convert_alpha()
        #personnages
        self.commercant = pygame.image.load("Personnage" + os.sep + "C" + os.sep + "perso.png").convert_alpha()
        self.perso_1_ = pygame.image.load("Personnage" + os.sep + "1" + os.sep + "perso_gauche.png").convert_alpha()
        self.perso_2_ = pygame.image.load("Personnage" + os.sep + "2" + os.sep + "perso_droite.png").convert_alpha()
        self.perso_3_ = pygame.image.load("Personnage" + os.sep + "3" + os.sep + "perso_gauche.png").convert_alpha()
        self.perso_4_ = pygame.image.load("Personnage" + os.sep + "4" + os.sep + "perso_droite.png").convert_alpha()
        self.perso_5_ = pygame.image.load("Personnage" + os.sep + "5" + os.sep + "perso_gauche.png").convert_alpha()
        self.perso_6_ = pygame.image.load("Personnage" + os.sep + "6" + os.sep + "perso_droite.png").convert_alpha()
        self.perso_7_ = pygame.image.load("Personnage" + os.sep + "7" + os.sep + "perso_gauche.png").convert_alpha()
        self.perso_8_ = pygame.image.load("Personnage" + os.sep + "8" + os.sep + "perso_droite.png").convert_alpha()
        #laines
        self.laine_b = pygame.image.load(self.texture_pack + "laine_bleue.png").convert()
        self.laine_g = pygame.image.load(self.texture_pack + "laine_gris.png").convert()
        self.laine_j = pygame.image.load(self.texture_pack + "laine_jaune.png").convert()
        self.laine_r = pygame.image.load(self.texture_pack + "laine_rose.png").convert()
        self.laine_ve = pygame.image.load(self.texture_pack + "laine_vert.png").convert()
        self.laine_vi = pygame.image.load(self.texture_pack + "laine_violet.png").convert()
        #potions
        self.potion_vie = pygame.image.load(self.texture_pack + "potion_vie.png").convert_alpha()
        self.potion_mana = pygame.image.load(self.texture_pack + "potion_mana.png").convert_alpha()
        #objets de mana
        self.mana_cone = pygame.image.load(self.texture_pack + "mana_cone.png").convert_alpha()
        self.mana_sphere = pygame.image.load(self.texture_pack + "mana_sphere.png").convert_alpha()
        self.mana_laser = pygame.image.load(self.texture_pack + "mana_laser.png").convert_alpha()
        self.mana_build = pygame.image.load(self.texture_pack + "mana_build.png").convert_alpha()
        self.mana_telep = pygame.image.load(self.texture_pack + "mana_telep.png").convert_alpha()
        self.mana_feu = pygame.image.load(self.texture_pack + "mana_feu.png").convert_alpha()
        #ajouts
        self.torche_b = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "torche_bleu.png").convert_alpha()
        self.torche_v = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "torche_vert.png").convert_alpha()
        self.torche_j = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "torche_jaune.png").convert_alpha()
        self.torche_r = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "torche_rouge.png").convert_alpha()
        self.jukebox = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "jukebox.png").convert_alpha()
        self.champi_b = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "champi_blanc.png").convert_alpha()
        self.champi_r = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "champi_rouge.png").convert_alpha()
        self.charbon = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "charbon.png").convert_alpha()
        self.diamant = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "diamand.png").convert_alpha()
        self.emeraude = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "emeraude.png").convert_alpha()
        self.or_ = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "or.png").convert_alpha()
        self.rubis = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "rubis.png").convert_alpha()
        self.fleur_b = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "fleur_bleu.png").convert_alpha()
        self.fleur_r = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "fleur_rouge.png").convert_alpha()
        self.fleur_j = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "fleur_jaune.png").convert_alpha()
        self.cd_jaune = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "cd_jaune.png").convert_alpha()
        self.cd_rose = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "cd_rose.png").convert_alpha()
        self.cd_vert = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "cd_vert.png").convert_alpha()
        self.cd_violet = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "cd_violet.png").convert_alpha()
        self.table_bleu = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_bleu.png").convert_alpha()
        self.table_gris = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_gris.png").convert_alpha()
        self.table_jaune = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_jaune.png").convert_alpha()
        self.table_marron = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_marron.png").convert_alpha()
        self.table_marronc = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_marronc.png").convert_alpha()
        self.table_marronf = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_marronf.png").convert_alpha()
        self.table_rouge = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_rouge.png").convert_alpha()
        self.table_vert = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "table_vert.png").convert_alpha()
        self.nucleaire = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "nucleaire.png").convert()
        self.teleporteur = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "telepo.png").convert_alpha()
        self.pierre_feu = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "pierre_feu.png").convert()
        self.pierre_eau = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "pierre_eau.png").convert()
        self.pierre_terre = pygame.image.load(self.texture_pack + "Nouveau" + os.sep + "pierre_terre.png").convert()
        self.echelle = pygame.image.load(self.texture_pack + "echelle.png").convert_alpha()
        self.monnaie_img = pygame.image.load(self.texture_pack + "monnaie.png").convert_alpha()
        self.marteau_img = pygame.image.load(self.texture_pack + "marteau.png").convert_alpha()
        self.pancarte = pygame.image.load(self.texture_pack + "pancarte.png").convert_alpha()
        self.time_telep = pygame.image.load(self.texture_pack + "time_telep.png").convert_alpha()
        self.feu = pygame.image.load("Particules" + os.sep + "feu.png").convert_alpha()
        #dico
        self.img_tous_blocs = {
            "q": self.bibli,
            "m": self.mur,
            "1": self.perso_1_,
            "t": self.toit,
            "d": self.sable,
            "2": self.perso_2_,
            "e": self.eau_,
            "s": self.sol,
            "3": self.perso_3_,
            "h": self.herbe,
            "a": self.mine_or,
            "4": self.perso_4_,
            "r": self.mine_c,
            "y": self.mine_d,
            "5": self.perso_5_,
            "u": self.mine_e,
            "i": self.mine_r,
            "6": self.perso_6_,
            "M": self.demi_sol,
            "v": self.verre,
            "7": self.perso_7_,
            "l": self.verre_b,
            "k": self.verre_j,
            "8": self.perso_8_,
            "g": self.verre_v,
            "f": self.verre_r,
            "x": self.briques,
            "b": self.mur2,
            "n": self.mur3,
            "?": self.demi_mur,
            ".": self.demi_mur2,
            "/": self.demi_mur3,
            "p": self.indes,
            "A": self.laine_b,
            "Z": self.laine_g,
            "E": self.laine_j,
            "R": self.laine_r,
            "T": self.laine_ve,
            "Y": self.laine_vi,
            "U": self.dirt,
            "I": self.neige,
            "O": self.tronc,
            "P": self.feuille,
            'Q': self.potion_vie,
            'S': self.potion_mana,
            'D': self.mana_laser,
            'F': self.mana_telep,
            'G': self.mana_feu,
            'H': self.mana_cone,
            'J': self.mana_sphere,
            'K': self.mana_build,
            "0": self.selection_bloc,
            'W': self.torche_b,
            'X': self.torche_v,
            'C': self.torche_j,
            'V': self.torche_r,
            'B': self.jukebox,
            'az': self.champi_b,
            'ze': self.champi_r,
            'er': self.charbon,
            'rt': self.diamant,
            'ty': self.emeraude,
            'yu': self.or_,
            'ui': self.rubis,
            'io': self.fleur_b,
            'op': self.fleur_r,
            'pq': self.fleur_j,
            'qs': self.cd_jaune,
            'sd': self.cd_rose,
            'df': self.cd_vert,
            'fg': self.cd_violet,
            'gh': self.table_bleu,
            'hj': self.table_gris,
            'jk': self.table_jaune,
            'kl': self.table_marron,
            'lm': self.table_marronc,
            'mw': self.table_marronf,
            'wx': self.table_rouge,
            'xc': self.table_vert,
            'c': self.commercant,
            'cv': self.nucleaire,
            'vb': self.teleporteur,
            'bn': self.pierre_eau,
            'n?': self.pierre_feu,
            '?.': self.pierre_terre,
            './': self.echelle,
            '/§': self.monnaie_img,
            '§%': self.marteau_img,
            '%a': self.pancarte,
            '%b': self.time_telep,
            'feu': self.feu
        }

    def get_img_dict(self):
        return self.img_tous_blocs

    def fire_bloc(self, pos_x, pos_y):
        self.bloc_fired = pos_x, pos_y
        self.start_fireing = time.time() + 0.125
        self.remove_bloc(pos_x, pos_y, 'feu')

    def show_fire(self):
        if time.time() > self.start_fireing and self.bloc_fired != (-1, -1):
            self.remove_bloc(self.bloc_fired[0], self.bloc_fired[1], '0')
            self.start_fireing = -1
            self.bloc_fired = -1, -1

    def set_meteo(self, command, rain=Weather(), wind=Weather(), storm=Weather()):
        if command == 'toggledownfalled':
            self.rain.do(command)
        if command == 'invert':
            self.wind.do(command)
        self.rain = rain
        self.wind = wind
        self.storm = storm

    def reload_map(self):
        if self.adresse != "":
            with open(self.adresse, 'rb') as map_reading:
                #self.carte = rle.RLEUncompress(map_reading).load()
                self.carte = pickle.Unpickler(map_reading).load()
                #self.carte = rle.load(map_reading)

    def render(self):
        debut_generation = time.time()
        self.show_fire()
        #fov[1] = fov[0] + self.nb_blocs_large
        structure = [line[self.fov[0]:self.fov[1]:] for line in self.carte]
        if structure != self.last_map_lst:
            self.last_map_lst = structure
            self.map_surf = pygame.Surface(self.ecran.get_size())
            #On blit le fond
            if not self.rain.get_action() or not self.wind.get_action() or not self.storm.get_action():
                self.map_surf.fill((76, 76, 76))
            else:
                self.map_surf.fill(self.couleur_fond)
            #On parcourt la liste du niveau
            for num_ligne in range(20):
                #On parcourt les listes de lignes
                for num_case in range(self.fov[1] - self.fov[0]):
                    #On calcule la position réelle en pixels
                    bloc_actuel = structure[num_ligne][num_case]
                    x = num_case * taille_sprite
                    y = num_ligne * taille_sprite
                    if bloc_actuel != '0':
                        if not self.marteau.has_been_2nd_planed(bloc_actuel):
                            self.map_surf.blit(self.img_tous_blocs[bloc_actuel], (x, y))
                        else:
                            self.map_surf.blit(self.img_tous_blocs[bloc_actuel[2::]], (x, y))
                            self.map_surf.blit(self.bleu_nuit_1, (x, y), special_flags=BLEND_RGBA_ADD)
            if self.current_shader == "standart":
                #standart
                ombrage_bloc(self.map_surf, structure, self.fov, self.blocs)
            elif self.current_shader == "progressif":
                #progressif
                ombrage_bloc2(self.map_surf, structure, self.fov, self.blocs)
            elif self.current_shader == "raycasté":
                #raycasté
                ombrage_bloc3(self.map_surf, structure, self.fov, self.blocs)
            elif self.current_shader == "gaussien":
                #ombres gaussiennes
                ombrage_bloc4(self.map_surf, structure, self.fov, self.blocs)
        else:
            self.ecran.blit(self.map_surf, (0, 0))

        #calcul et affichage du temps de génération du terrain
        #generation = "Terrain généré en %3.3f millisecondes" % ((time.time() - debut_generation) * 1000)
        #affichage du shader en cours d'utilisation
        rendu_shader = font.render("Shader :: " + self.current_shader, 1, (10, 10, 10))
        pygame.draw.rect(self.root, (0, 0, 0), (105, 9, 250, 19))
        pygame.draw.rect(self.root, (150, 150, 150), (105, 9, rendu_shader.get_size()[0] + 12, 19))
        self.root.blit(rendu_shader, (111, 10))
        if self.rain.get_action():
            self.rain.update()
        if self.wind.get_action():
            self.wind.update()
        if self.storm.get_action():
            self.storm.update()

    def collide(self, x, y):
        collision = False
        if 0 <= y <= self.y_max and 0 <= x <= self.x_max:
            if self.carte[y][x] in self.collision_bloc and self.carte[y][x] != './':
                collision = True
            else:
                collision = False
        return collision

    def set_texture_pack(self, txt_pack):
        self.texture_pack = txt_pack

    def get_texture_pack(self):
        return self.texture_pack

    def get_tile(self, x, y):
        if 0 <= x <= self.get_x_len() and 0 <= y <= self.get_y_len():
            return self.carte[y][x]
        return '0'

    def get_y_len(self):
        return len(self.carte)

    def get_x_len(self):
        return len(self.carte[0])

    def get_list(self):
        return self.carte

    def remove_bloc(self, x, y, new):
        self.carte[y][x] = new
        self.new_bloc = True

    def get_fov(self):
        return self.fov

    def set_fov(self, first_fov, last_fov):
        if first_fov >= 0:
            self.fov = [first_fov, last_fov]
            return True
        return False

    def get_space(self):
        return self.fov[1] - self.fov[0]

    def switch_shader(self):
        self.compteur_shader += 1
        self.current_shader = self.liste_shader[self.compteur_shader % len(self.liste_shader)]

    def set_current_shader(self, shader):
        self.current_shader = shader

    def get_curent_shader(self):
        return self.current_shader

    def set_background_color(self, color):
        self.couleur_fond = color

    def get_background_color(self):
        return self.couleur_fond

    def gravity_for_entity(self):
        structure = [line[self.fov[0]:self.fov[1]:] for line in self.carte]
        for y in range(len(structure)):
            for x in range(len(structure[0])):
                bloc = structure[y][x]
                if bloc in self.gravity_entity and y + 1 <= len(structure) - 1:
                    if structure[y+1][x] == '0':
                        self.carte[y+1][x + self.fov[0]], self.carte[y][x + self.fov[0]] = \
                            self.carte[y][x + self.fov[0]], self.carte[y+1][x + self.fov[0]]

    def save(self):
        with open(self.adresse, "wb") as map_writing:
            #rle.RLECompress(map_writing).dump(self.carte)
            pickle.Pickler(map_writing).dump(self.carte)
            #rle.dump(map_writing, self.carte)
        if self.new_bloc:
            numero_carte = str(len(glob.glob('Niveaux' + os.sep + 'Olds Maps' + os.sep + '*.lvl')) + 1)
            if int(numero_carte) <= 9999:
                numero_carte = '0' * (4 - len(numero_carte)) + numero_carte
                with open('Niveaux' + os.sep + 'Olds Maps' + os.sep + 'map' + numero_carte + '.lvl', 'wb') as old_map_write:
                    #rle.RLECompress(old_map_write).dump(self.carte)
                    pickle.Pickler(old_map_write).dump(self.carte)
                    #rle.dump(old_map_write, self.carte)


class LANMap(Carte):
    def __init__(self, surface, surface_mere, marteau, nb_blocs_large, socket, params, blocs, rain=None, wind=None, storm=None):
        super().__init__(surface, surface_mere, marteau, nb_blocs_large, blocs, rain=rain, wind=wind, storm=storm)
        self.blocs = blocs
        self.ecran = surface
        self.root = surface_mere
        self.marteau = marteau
        self.nb_blocs_large = nb_blocs_large
        self.socket = socket
        self.params = params
        self.buffer_size = 4096

    def receive_map(self):
        self.socket.sendto(pickle.dumps("map->" + str(self.fov[0]) + ":" + str(self.fov[1])), self.params)
        temp = self.socket.recv(self.buffer_size)
        temp = pickle.loads(temp)
        if type(temp) == list:
            self.carte = temp
        elif type(temp) == dict:
            self.carte[temp.keys()[0][1]][temp.keys()[0][0]] = temp[temp.keys()[0]]

    def remove_bloc(self, x, y, new):
        self.socket.sendto(pickle.dumps("set->" + str(x) + ":" + str(y) + ":" + str(new)), self.params)

    def get_tile(self, x, y):
        self.socket.sendto(pickle.dumps("get->" + str(x) + ":" + str(y)), self.params)
        return pickle.loads(self.socket.recv(self.buffer_size))

    def make_choice_oth(self, print_oth):
        self.print_oth = print_oth

    def render(self):
        debut_generation = time.time()
        #fov[1] = fov[0] + self.nb_blocs_large
        structure = self.carte
        #On blit le fond
        if self.rain != None or self.wind != None or self.storm != None:
            pygame.draw.rect(self.ecran, (76, 76, 76), (0, 0, (self.fov[1] - self.fov[0]) * 30, 600))
        else:
            pygame.draw.rect(self.ecran, self.couleur_fond, (0, 0, (self.fov[1] - self.fov[0]) * 30, 600))
        #On parcourt la liste du niveau
        for num_ligne in range(20):
            #On parcourt les listes de lignes
            for num_case in range(self.fov[1] - self.fov[0]):
                #On calcule la position réelle en pixels
                bloc_actuel = structure[num_ligne][num_case]
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite
                if bloc_actuel != '0':
                    if not self.marteau.has_been_2nd_planed(bloc_actuel):
                        self.ecran.blit(self.img_tous_blocs[bloc_actuel], (x, y))
                    else:
                        self.ecran.blit(self.img_tous_blocs[bloc_actuel[2::]], (x, y))
                        self.ecran.blit(self.bleu_nuit_1, (x, y), special_flags=BLEND_RGBA_ADD)
        if self.current_shader == "standart":
            #standart
            ombrage_bloc(self.ecran, structure, self.fov, self.blocs)
        elif self.current_shader == "progressif":
            #progressif
            ombrage_bloc2(self.ecran, structure, self.fov, self.blocs)
        elif self.current_shader == "raycasté":
            #raycasté
            ombrage_bloc3(self.ecran, structure, self.fov, self.blocs)
        elif self.current_shader == "gaussien":
            #ombres gaussiennes
            ombrage_bloc3(self.ecran, structure, self.fov, self.blocs)

        if self.print_oth:
            self.socket.sendto(pickle.dumps("get->others"), self.params)
            temp = self.socket.recv(4096)
            temp = pickle.loads(temp)
            #x
            #y
            #pseudo -> (x_perso - len(pseudo), y_perso - 12)
            #représentation
            #situation actuelle
            #couleur pseudo
            for i in range(len(temp)):
                x = (temp[i][0] - self.get_fov()[0]) * 30
                y = temp[i][1] * 30
                pseudo_str = temp[i][2]
                pseudo_oth = font.render(temp[i][2], 1, temp[i][5])
                situation = temp[i][4]
                if situation == 1:
                    situation = "perso_droite.png"
                else:
                    situation = "perso_gauche.png"
                perso_oth = pygame.image.load("Personnage" + os.sep + temp[i][3] + situation).convert_alpha()
                self.ecran.blit(perso_oth, (x, y))
                self.ecran.blit(pseudo_oth, (x - len(pseudo_str), y - 12))

        #calcul et affichage du temps de génération du terrain
        #generation = "Terrain généré en %3.3f millisecondes" % ((time.time() - debut_generation) * 1000)
        #pygame.draw.rect(self.root, (150, 150, 150), (6, 5, 265, 19))
        #self.root.blit(font.render(generation, 1, (10, 10, 10)), (12, 6))
        #affichage du shader en cours d'utilisation
        rendu_shader = font.render("Shader :: " + self.current_shader, 1, (10, 10, 10))
        pygame.draw.rect(self.root, (0, 0, 0), (105, 9, 250, 19))
        pygame.draw.rect(self.root, (150, 150, 150), (105, 9, rendu_shader.get_size()[0] + 12, 19))
        self.root.blit(rendu_shader, (111, 10))
        if self.rain.get_action():
            self.rain.update()
        if self.wind.get_action():
            self.wind.update()
        if self.storm.get_action():
            self.storm.update()

    def collide(self, x, y):
        collision = False
        x -= self.fov[0]
        if 0 <= y <= self.y_max and 0 <= x <= self.x_max:
            if self.carte[y][x] in self.collision_bloc and self.carte[y][x] != './':
                collision = True
            else:
                collision = False
        return collision

    def save(self):
        self.socket.sendto(pickle.dumps("save"), self.params)