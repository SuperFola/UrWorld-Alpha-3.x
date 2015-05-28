#-*-coding: utf8-*

from   constantes import *
import sys
import re
import os

#max = 1.3407807929942597e+154 : 2**2**2**2**2**2**2**2**2**2

def bdd_connexion(envoyer, pseudo, ad_mac, niv_courant = 1, monnaie = 5000):
	temporaire = ""
	pseudo_recup = str(pseudo)
	if envoyer.lower() == "intercalere1":
		#on ajoute la personne
		ajouter = pseudo + ";" + str(ad_mac) + ";" + str(niv_courant) + ";" + str(monnaie)
		with open("Parties" + os.sep + "intercalere.sav", "w+") as ajout:
			ajout.write(ajouter + "\n")
		with open("Parties" + os.sep + "pseudo.sav", "w+") as ajout_p:
			ajout_p.write(pseudo)
	elif envoyer.lower() == "intercalere2":
		"""
		connexion avec l'algo d'intercalaires
		"""
		try:
			intercalere = ""
			with open("Parties" + os.sep + "intercalere.sav", "r") as recupere_intercalere:
				#intercalere = recupere_intercalere.read()
				for ligne in recupere_intercalere:
					ligne_ = []
					if ligne != "\n":
						ligne_.append(ligne)
				print(ligne_)
				#bon oki ici il faut que j'arrive à récupérer qu'une seule ligne . . .
				for result in ligne_:
					if re.search(r"" + pseudo + "", result) is not None:
						temporaire = result #ma ligne
				#décalage normal,on n'exécute pas dans le for :)
				temporaire.split(';')
				pseudo_intercalere      = temporaire.split(';')[0:1]
				ad_mac_intercalere      = temporaire.split(';')[1:2]
				niv_courant_intercalere = temporaire.split(';')[2:3]
				monnaie_intercalere     = temporaire.split(';')[3:4]
				tresors_inter = []
				nourriture_ecrire = []
				objet_inter = []
				if pseudo == pseudo_intercalere and ad_mac == ad_mac_intercalere:
					#tout est ok
					if os.path.exists("Parties" + os.sep + "sac.sav") and os.path.exists("Parties" + os.sep + "equipement_en_cours.sav") \
					and os.path.exists("Parties" + os.sep + "monnaie.sav") and os.path.exists("Parties" + os.sep + "tresors.sav")        \
					and os.path.exists("Parties" + os.sep + "nourriture.sav") and os.path.exists("Parties" + os.sep + "objets.sav")      \
					and os.path.exists("Parties" + os.sep + "niveau.sav"):
						with open("Parties" + os.sep + "monnaie.sav", "wb+") as monaie_fichier:
							mon_pickler_3 = pickle.Pickler(monaie_fichier)
							mon_pickler_3.dump(monnaie_intercalere)
						with open("Parties" + os.sep + "tresors.sav", "wb+") as tresors_fichier:
							mon_pickler_4 = pickle.Pickler(tresors_fichier)
							mon_pickler_4.dump(tresors_inter)
						with open("Parties" + os.sep + "nourriture.sav", "wb+") as nourriture_ecrire:
							mon_pickler_5 = pickle.Pickler(nourriture_ecrire)
							mon_pickler_5.dump(nourriture_inter)
						with open("Parties" + os.sep + "objets.sav", "wb+") as objet_ecrire:
							mon_pickler_6 = pickle.Pickler(objet_ecrire)
							mon_pickler_6.dump(objet_inter)
						with open("Parties" + os.sep + "niveau.sav", "wb+") as niv_ecrire:
							mon_pickler_7 = pickle.Pickler(niv_ecrire)
							mon_pickler_7.dump(niv_courant_intercalere)
				else: sys.exit()
				"""
				ci dessus il faudra récupérer le pseudo, adresse mac, et stocker le numero niveau + sac
				dans les fichiers en les stockant dans la bdd avant puis on vide les fichiers
				"""
		except Exception as err:
			print(err)
			input()