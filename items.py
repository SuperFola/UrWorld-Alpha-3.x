# -*-coding: utf8-*

import commerces_p as cmp
import pygame as pg
import os

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