import os
import pygame
from pygame.locals import *


class Water:
    def __init__(self, ecran, carte):
        self.ecran = ecran
        self.carte = carte
        self.eau = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "eau.png").convert_alpha()
        self._img = []
        self.velocity = 0.5
        self.time = 0
        self.draw_overlay()

    def draw_overlay(self):
        for i in range(30):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.eau, (self.time - self.eau.get_width(), 0))
            self.surf.blit(self.eau, (self.time, 0))

            self.surf.convert_alpha()

            self.time += self.velocity
            self.time %= self.eau.get_width()
            self._img.append(self.surf)
        self.time = 0

    def draw(self):
        self.time += self.velocity
        crt = self.carte.get_map_fov()
        for y in range(len(crt)):
            for x in range(len(crt[y])):
                if crt[y][x] == 'e':
                    self.ecran.blit(self._img[self.time % len(self._img)], (x * 30, y * 30))

    def update(self):
        self.draw()