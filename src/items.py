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


class Marteau:
    def __init__(self, rcenter, surface, font):
        self.life = 100
        self.max_life = 100
        self.rcenter = rcenter
        self.ecran = surface
        self.font = font
        self.loadbar = pg.image.load(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Bar" + os.sep + "imgo3.png").convert_alpha()

    def utiliser(self, carte, y_clic, x_clic):
        if self.life >= 0.25:
            if carte.get_tile(x_clic, y_clic)[:2:] != '0+':
                if self.life:
                    carte.remove_bloc(x_clic, y_clic, '0+' + carte.get_tile(x_clic, y_clic))
            else:
                if self.life:
                    carte.remove_bloc(x_clic, y_clic, carte.get_tile(x_clic, y_clic)[2::])
        else:
            cmp.message_affiche("Votre marteau n'a plus de vie, impossible de l'utiliser maintenant !", self.rcenter)
        self.life -= 1 if self.life - 1 >= 0 else 0

    def has_been_2nd_planed(self, bloc):
        return True if bloc[:2:] == '0+' else False

    def update(self):
        self.life = self.life + 0.045 if self.life + 0.045 <= self.max_life else self.max_life

    def render(self):
        texte_marteau = self.font.render('Energie du marteau : %3i' % self.life, 1, (10, 10, 10))
        pg.draw.rect(self.ecran, (20, 180, 20), (self.rcenter[0] - self.loadbar.get_size()[0] // 2 + 3, 7, int(self.life * 2.5), 14))
        self.ecran.blit(self.loadbar, (self.rcenter[0] - self.loadbar.get_size()[0] // 2, 5))
        self.ecran.blit(texte_marteau, (self.rcenter[0] - self.loadbar.get_size()[0] // 2 + 3 + (244 - texte_marteau.get_size()[0]), 6))