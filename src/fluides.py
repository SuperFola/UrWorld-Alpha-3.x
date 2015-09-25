import os
import pygame
from pygame.locals import *


class Water:
    def __init__(self, ecran, carte):
        self.ecran = ecran
        self.carte = carte
        self.eau = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "eaumvt.png").convert_alpha()
        self.eaunrmlt = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "eau.png").convert_alpha()
        self._img = []
        self._img2 = []
        self.velocity = 0.5
        self.time = 0
        self.draw_overlay()

    def draw_overlay(self):
        for i in range(60):
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

        for i in range(60):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.eaunrmlt, (self.time - self.eaunrmlt.get_width(), 0))
            self.surf.blit(self.eaunrmlt, (self.time, 0))

            self.surf.convert_alpha()

            self.time += self.velocity
            self.time %= self.eaunrmlt.get_width()
            self._img2.append(self.surf)
        self.time = 0

    def draw(self):
        self.time += self.velocity
        crt = self.carte.get_map_fov()
        for y in range(len(crt)):
            for x in range(len(crt[y])):
                if y - 1 >= 0:
                    if crt[y-1][x] == 'e' and crt[y][x] == 'e':
                        self.ecran.blit(self._img2[int(self.time % len(self._img))], (x * 30, y * 30))
                    elif crt[y-1][x] != 'e' and crt[y][x] == 'e':
                        self.ecran.blit(self._img[int(self.time % len(self._img2))], (x * 30, y * 30))
                else:
                    if crt[y][x] == 'e':
                        self.ecran.blit(self._img[int(self.time % len(self._img2))], (x * 30, y * 30))

    def update(self):
        self.draw()