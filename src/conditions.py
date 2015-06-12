# -*- coding: utf-8 -*-

import random
import structs as st
import properties as property
from blocks import *


def TREE(map_, pos):
    x, y = pos
    if map_[x, y+1]\
            and map_[x+1, y+1]\
            and not map_[x, y]\
            and not map_[x+1, y]:
        tree = random.randint(0, 1000) in range(property.tree_rate)
        return tree

def HOUSE(map_, pos):
    x, y = pos
    if map_[x-3, y+1] \
            and map_[x-2, y+1]\
            and map_[x-1, y+1]\
            and map_[x, y+1]\
            and map_[x+1, y+1]\
            and map_[x+2, y+1]\
            and map_[x+3, y+1]\
            and map_[x-3, y] \
            and not map_[x-2, y]\
            and not map_[x-1, y]\
            and not map_[x, y]\
            and not map_[x+1, y]\
            and not map_[x+2, y]\
            and not map_[x+3, y]:
        return random.randint(0, 1000) in range(property.house_rate)

def PONT(map_, pos):
    x, y = pos
    on_y_va = False
    for y, ligne in enumerate(st.PONT.__repr__()):
        for x, element in enumerate(ligne):
            if element is not None:
                if map_[x, y] in (AIR, GRASS, DIRT):
                    on_y_va = True
                else:
                    on_y_va = False
                    break
    if on_y_va and \
            map_[x, y+11] in (GRASS, DIRT) and \
            map_[x+1, y+11] in (GRASS, DIRT) and \
            map_[x+2, y+11] in (GRASS, DIRT) and \
            map_[x+3, y+11] in (GRASS, DIRT) and \
            map_[x+4, y+11] in (GRASS, DIRT) and \
            map_[x+5, y+11] in (GRASS, DIRT) and \
            map_[x+6, y+11] in (GRASS, DIRT) and \
            map_[x+7, y+11] in (GRASS, DIRT) and \
            map_[x+8, y+11] in (GRASS, DIRT) and \
            map_[x+9, y+11] in (GRASS, DIRT) and \
            map_[x+10, y+11] in (GRASS, DIRT) and \
            map_[x+11, y+11] in (GRASS, DIRT) and \
            map_[x+12, y+11] in (GRASS, DIRT) and \
            map_[x+13, y+11] in (GRASS, DIRT):
        return random.randint(0, 1000) in range(property.pont_rate)

def LAKE(map_, pos):
    x, y = pos
    if map_[x+2, y] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+1, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+2, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+3, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+4, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+5, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+6, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+8, y+1] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+0, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+1, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+2, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+3, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+6, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+8, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+9, y+2] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+1, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+2, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+3, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+4, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+5, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+6, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+8, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+9, y+3] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+1, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+2, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+3, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+4, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+5, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+6, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+8, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x, y+4] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+1, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+2, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+3, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+4, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+5, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+6, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+7, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+8, y+5] in (DIRT, STONE, GRASS, SNOW) \
            and map_[x+9, y+5] in (DIRT, STONE, GRASS, SNOW):
        return random.randint(0, 1000) in range(property.lake_rate)