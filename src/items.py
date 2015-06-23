# -*-coding: utf8-*

import commerces_p as cmp
import pygame as pg
import pickle
import os


class DustElectricityDriven:
    def __init__(self, carte, font, surface, en_reseau=False):
        self.stop_conduct_after = 12  # blocks
        self.en_reseau = en_reseau
        self.carte = carte
        self.font = font
        self.ecran = surface
        self.cable = 'ccc'
        self.interrup_off = 'bbb'
        self.interrup_on = 'aaa'
        self.light_off = 'eee'
        self.light_on = 'ddd'
        self.repeteur = 'fff'
        self.piston = 'hhh'
        self.piston_collant = 'iii'
        self.all = [
            self.cable,
            self.interrup_off,
            self.interrup_on,
            self.light_off,
            self.light_on,
            self.repeteur
        ]
        self.road_map = []
        for i in self.carte.get_list():
            line = []
            for j in i:
                if j != '0' and j not in self.all:
                    line.append('1')
                else:
                    line.append(j)
            self.road_map.append(line)
    
    def get_built_tiles(self):
        return self.all

    def put(self, objet, x, y):
        if not self.en_reseau:
            self.road_map[y][x] = objet
        else:
            self.road_map[y][x - self.carte.get_first_fov()] = objet

    def put_cable(self, x, y):
        self.carte.remove_bloc(x, y, self.cable)
        self.put(self.cable, x, y)

    def put_interrupt(self, x, y, reverse=False):
        if not reverse:
            tile = self.interrup_off
        else:
            tile = self.interrup_on
        self.carte.remove_bloc(x, y, tile)
        self.put(tile, x, y)

    def put_light(self, x, y, reverse=False):
        if not reverse:
            tile = self.light_off
        else:
            tile = self.light_on
        self.carte.remove_bloc(x, y, tile)
        self.put(tile, x, y)

    def check_all(self):
        interruptors = []
        cables = []
        lights = []
        for i in range(0, 19):
            for j in range(self.carte.get_first_fov(-2), self.carte.get_last_fov(+2)):
                tile = self.carte.get_tile(j, i)
                if tile == self.interrup_on or tile == self.interrup_off:
                    state = 0 if tile == self.interrup_off else 1
                    interruptors.append([(j, i), state])
        for k in range(0, 19):
            for l in range(self.carte.get_first_fov(-2), self.carte.get_last_fov(+2)):
                for m in interruptors:
                    pass

    def right_click(self, x, y):
        tile = self.carte.get_tile(x, y)
        if tile in self.all:
            if tile == self.interrup_off:
                self.put_interrupt(x, y, reverse=True)
            if tile == self.interrup_on:
                self.put_interrupt(x, y)
            if tile == self.light_off:
                self.put_light(x, y, reverse=True)
            if tile == self.light_on:
                self.put_light(x, y)
            self.check_all()


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