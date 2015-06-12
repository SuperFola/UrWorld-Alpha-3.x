# -*- coding: utf-8 -*-

import pygame

surface = 0 #définition d'une valeur par défaut

#la fonction ne prendre comme argument que 'surface'
def fonction(surface):
    pygame.draw.rect(surface, (0, 0, 0), (0, 0, 150, 150))
    print('in sample')