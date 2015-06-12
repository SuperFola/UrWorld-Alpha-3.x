# -*-coding: utf8-*

import commerces_p as cmp
import pygame as pg
import os


class DustElectricityDriven:
    def __init__(self, carte, font, surface):
        self.stop_conduct_after = 12  # blocks
        self.carte = carte
        self.font = font
        self.ecran = surface
        self.cable = ''
        self.interrup_off = ''
        self.interrup_on = ''
        self.light_off = ''
        self.light_on = ''
        self.all = [
            self.cable,
            self.interrup_off,
            self.interrup_on,
            self.light_off,
            self.light_on
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

    def put_cable(self, x, y):
        self.carte.remove_bloc(x, y, self.cable)
        self.road_map[y][x] = self.cable

    def put_interrupt(self, x, y, reverse=False):
        if not reverse:
            tile = self.interrup_off
        else:
            tile = self.interrup_on
        self.carte.remove_bloc(x, y, tile)
        self.road_map[y][x] = tile

    def put_light(self, x, y, reverse=False):
        if not reverse:
            tile = self.light_off
        else:
            tile = self.light_on
        self.carte.remove_bloc(x, y, tile)
        self.road_map[y][x] = tile

    def check_all(self):
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


class Marteau:
    def __init__(self, rcenter, surface, font):
        self.life = 100
        self.max_life = 100
        self.rcenter = rcenter
        self.ecran = surface
        self.font = font
        self.loadbar = pg.image.load("Particules" + os.sep + "imgo3.png").convert_alpha()

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