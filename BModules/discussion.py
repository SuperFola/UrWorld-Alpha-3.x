#-*-coding: utf8-*

import  re
import  os
import  sys
import  time
import  pygame
import  random
import  socket
import  subprocess
import  platform        as     p
# import  win32com.client as     com
from    threading       import Thread
from    pygame.locals   import *
from    tkinter         import *

"""
def sizeToOctetKoMoGo(size):
	if size < 1024:
		return str(round(size / 1024.0)) + " Octets"
	elif size < 1024**2:
		return str(round(size / 1024.0, 3)) + " Ko"
	elif size < 1024**3:
		return str(round(size / (1024.0**2), 3)) + " Mo"
	else:
		return str(round(size / (1024.0**3), 3)) + " Go"

def totalSize(drive):
	fso = com.Dispatch("Scripting.FileSystemObject")
	drv = fso.GetDrive(drive)
	return drv.TotalSize

def freeSpace(drive):
	fso = com.Dispatch("Scripting.FileSystemObject")
	drv = fso.GetDrive(drive)
	return drv.FreeSpace
"""
def client_message():
	en_reseau = True
	port = 50000
	hote = "192.168.1.13"
	defhote = "127.0.0.1"
	def verif_all():
		if port_co.get().strip() != "" and port_co.get().isdigit():
			port = int(port_co.get())
		else:
			port = def_hote
		if hote_co.get().strip() != "":
			hote = hote_co.get()
		fenetre.destroy()
	fenetre = Tk()
	fenetre.title("UrWorld - Réseau")
	fenetre.resizable(False, False)
	Label(fenetre, text="****** Client UrWorld, bienvenue. ******").pack()
	Label(fenetre, text="").pack()
	Label(fenetre, text="Entrez l'adresse IP de l'ordinateur hôte :").pack()
	hote_co  = StringVar()
	try:
		defhote = socket.gethostbyname(socket.gethostname())
		hote_co.set(defhote)
	except NameError as nom_err:
		print(nom_err)
	except TypeError as type_err:
		print(type_err)
	Champ = Entry(fenetre, textvariable=hote_co)
	Champ.focus_set()
	Champ.pack()
	Label(fenetre, text="").pack()
	Label(fenetre, text="Entrez le port auquel se connecter :").pack()
	port_co = StringVar()
	port_co.set('50000')
	Champ_port = Entry(fenetre, textvariable=port_co)
	Champ_port.pack()
	Label(fenetre, text="").pack()
	Bouton = Button(fenetre, text ='Connexion', command = verif_all).pack()
	Label(fenetre, text="").pack()
	fenetre.mainloop()
	# print("_" * 80 + "|/-\\" * (81 // 4) + "|   " * (81 // 4))
	# os.system(os_clear_command) #on efface l'écran
	id_co_individuel = 0
	msg_a_envoyer = ""
	ligne_a_ajouter = ""
	msg_a_encoder = ""

	def async_recv(client_socket):
		while 1:
			msg_recu = client_socket.recv(1024)
			if msg_recu == b"":
				client_socket.close()
				print("Le serveur est arrêté.\n")
				break
			if msg_recu != msg_a_encoder:
				msg_recu = msg_recu.decode()
				if re.search(r'^id_', msg_recu) is None:
					print("\n>>>{0}".format(msg_recu))
				else:
					id_co_individuel = int(re.sub(r'(id_)', r'', msg_recu))
			elif msg_a_encoder == msg_recu:
				msg_recu = msg_recu.decode()
				print("\n>>>Envoyé : {0}".format(msg_recu))

	def envoie(*msg_a_envoyer):
		msg_a_encoder = str('-'.join(list(msg_a_envoyer)))
		msg_a_encoder = msg_a_encoder.encode()
		print(". . .")
		#on envoie le message
		connexion_avec_serveur.send(msg_a_encoder)
		msg_a_encoder   = ""

	result         = subprocess.Popen(['ipconfig', '/all'],stdout=subprocess.PIPE).stdout.read()
	adresse_mac    = re.search('([0-9A-F]{2}-?){6}', str(result)).group()
	adresse_mac    = adresse_mac.split('-')
	adresse_mac    = ':'.join(adresse_mac)
	nom_de_session = os.getenv("USERNAME")
	hote    = socket.gethostbyname(socket.gethostname())
	drive   = 'C:/'
	cpu_corps = str(os.cpu_count())
	systeme = p.system()
	python  = p.python_version()
	jeu, formatFichier = p.architecture()
	distribution = p.version()
	print("\t[*] " + "Système      Opérant     ::   " + systeme)
	print("\t[*] " + "Nombre Coeurs Processeur ::   " + cpu_corps, end = '   ')
	print("-   Correct" if int(cpu_corps) >= 2 else "-   Insuffisant")
	print("\t[*] " + "Architecture Processeur  ::   " + jeu)
	print("\t[*] " + "Version      Système     ::   " + distribution)
	print("\t[*] " + "Version      Python      ::   " + python)
	print("\t[*] " + "Adresse      IP          ::   " + hote)
	print("\t[*] " + "Adresse      MAC         ::   " + adresse_mac)
	"""print("\t[*] " + "C:/  Espace  Total       ::   " + sizeToOctetKoMoGo(totalSize(drive)))
	print("\t[*] " + "C:/  Espace  Libre       ::   " + sizeToOctetKoMoGo(freeSpace(drive)))"""
	print("\t[*] " + "Session      Active      ::   " + nom_de_session)
	print("")

	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Connection sur le serveur {0} au port {1} . . .\n".format(hote, port))
	connexion_avec_serveur.connect((hote, port))

	#envoie(systeme);envoie(jeu);envoie(distribution);envoie(python);envoie(hote);envoie(adresse_mac);envoie(nom_de_session)
	envoie(nom_de_session, nom_de_session)
	
	# faire la réception du socket dans un autre thread
	thread =  Thread(target=async_recv, args = (connexion_avec_serveur,))
	thread.start()

	print("Connexion établie avec le serveur sur le port {}.".format(port))

	while msg_a_envoyer.lower() != "fin":
		try:
			#partie du code où on va écrire un message pour le client
			while 1:
				ligne_a_ajouter = input("> ")
				if ligne_a_ajouter == "send": #la commande 'fin' demande l'arrêt du serveur ;)
					break
				elif re.search(r'send$', ligne_a_ajouter) is not None:
					break
				elif ligne_a_ajouter.lower() == "fin":
					#on arrete tout :
					break
				elif ligne_a_ajouter == "ren":
					msg_a_envoyer += "\n"
					msg_a_envoyer += ligne_a_ajouter
					ligne_a_ajouter = ""
					envoie(msg_a_envoyer)
					msg_a_envoyer = ""
				elif ligne_a_ajouter == "id":
					msg_a_envoyer += "\n"
					msg_a_envoyer += ligne_a_ajouter
					ligne_a_ajouter = ""
					envoie(msg_a_envoyer)
					msg_a_envoyer = ""
				else:
					msg_a_envoyer += "\n"
					msg_a_envoyer += ligne_a_ajouter
					ligne_a_ajouter = ""

			if msg_a_envoyer != "" and ligne_a_ajouter.lower() != "fin" and ligne_a_ajouter != "ren":
				#on envoie
				envoie(msg_a_envoyer)
				msg_a_envoyer = ""
			#--------------------------------------------------------
			elif ligne_a_ajouter.lower() == "fin":
				msg_a_envoyer = "fin"
				msg_a_encoder = msg_a_envoyer.encode()
				connexion_avec_serveur.send(msg_a_encoder)
				break
			#--------------------------------------------------------
		except NameError as nom_erreur:
			print(nom_erreur)
			with open('log.log', 'a') as log:
				log.write("\n" + nom_erreur)

		except TypeError as type_err:
			print(type_err)
			with open('log.log', 'a') as log:
				log.write("\n" + type_err)

		except EnvironmentError as env_err:
			print(env_err)
			with open('log.log', 'a') as log:
				log.write("\n" + env_err)

		except Exception as exc:
			print(exc)
			with open('log.log', 'a') as log:
				log.write("\n" + exc)

	thread.stop()
	print("Fermeture de la connexion. Appuyer sur une touche pour continuer . . .")
	wait = input()
	connexion_avec_serveur.close()

if __name__ == "__main__":
	client_message()