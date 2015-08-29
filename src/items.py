# -*-coding: utf8-*

import commerces_p as cmp
import pygame as pg
import pickle
import os


class Conteneur:
    def __init__(self):
        self.conteneurs = []
        self.code_tile = 'jjj'
    
    def load(self):
        if os.path.exists(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "conteneurs.sav"):
            with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "conteneurs.sav", "rb") as file:
                self.conteneurs = pickle.Unpickler(file).load()
    
    def save(self):
        with open(".." + os.sep + "assets" + os.sep + "Save" + os.sep + "conteneurs.sav", "wb") as cwriteb:
            pickle.Pickler(cwriteb).dump(self.conteneurs)
    
    def test(self, x, y):
        for h in self.conteneurs:
            if h[0] == (x, y):
                return True
        return False
    
    def add_on_existing(self, x, y, bloc):
        for i in self.conteneurs:
            if i[0] == (x, y):
                i[1].append(bloc)
                break
    
    def add_new(self, x, y):
        self.conteneurs.append([(x, y), ['jjj']])
    
    def destroy_last_bloc(self, x, y):
        bloc = ''
        cout = 0
        while cout < len(self.conteneurs):
            if self.conteneurs[cout][0] == (x, y):
                bloc = self.conteneurs[cout][1].pop(-1)
                break
            cout += 1
        if bloc == '':
            if self.destroy_conteneur(x, y):
                bloc = 'jjj'
        return bloc
    
    def destroy_conteneur(self, x, y):
        for j in range(len(self.conteneurs)):
            if self.conteneurs[j][0] == (x, y):
                self.conteneurs.pop(j)
                return True
        return False
    
    def list_conteners_pos_and_tile(self):
        liste = []
        for k in self.conteneurs:
            if k[1] != []:
                liste.append([k[0], k[1][-1]])
            else:
                self.destroy_conteneur(k[0][0], k[0][1])
        return liste