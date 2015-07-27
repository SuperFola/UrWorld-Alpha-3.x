import os
import re
import time
import pickle
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connect = 1
BUFFER = 4096

hote = input("Entrez l'hote auquel se connecter > ")
while not re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', hote):
    hote = input("Entrez l'hote auquel se connecter > ")
port = input("Entrez le port par lequel se connecter > ")
while not port.isdigit():
    port = input("Entrez le port par lequel se connecter > ")
port = int(port)

params = (hote, port)

pseudo = input("Pseudonyme > ")
mot_de_passe = input("Mot de passe > ")
os.system('cls')

print("""Hote: %s
Port: %i
Pseudonyme: %s
Heure: %s
Socket: %s
""" % (hote, port, pseudo, time.asctime(), sock.getsockname()))

sock.sendto(pickle.dumps([pseudo, True, True, False]), params)
sock.sendto(pickle.dumps(mot_de_passe), params)
if not sock.recv(BUFFER):
    connect = 0

while connect:
    input_usr = input("$ ")
    sock.sendto(pickle.dumps(input_usr), params)
    datas = pickle.loads(sock.recv(BUFFER))
    print(datas)

print("Vous avez été deconnecté ...\n")
input("Appuyez sur Entrée pour terminer le programme ...")