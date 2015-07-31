#C:\Python34\python.exe
# -*- coding: utf-8 -*-

import random
from structs import *

BLOCK, VOID = True, False

foret = {
    'stone': ['s'],
    'snow': ['I'],
    'grass': ['h'],
    'dirt': ['U']
}
desert = {
    'stone': ['s'],
    'snow': ['d'],
    'grass': ['d'],
    'dirt': ['d']
}
noman_land = {
    'stone': ['s'],
    'snow': ['I'],
    'grass': ['az', 'ze'] + ['U'] * 48,
    'dirt': ['U']
}

tundra = {
    'stone': ['s'],
    'snow': ['I'],
    'grass': ['I'],
    'dirt': ['I']
}

mineral_world = {
    'stone': ['s'] * 15 + ['a', 'r', 'u', 'y', 'i'],
    'snow': ['s'],
    'grass': ['h'],
    'dirt': ['U']
}

class Map(list):
    def __init__(self, length, flatness, height=range(1, 16), headstart=8, deniv=1, structs=Structure.structures):
        self.structs = structs
        self.current_biome_size = 0
        self.current_biome = 0
        self.liste_biomes = [
            foret,
            desert,
            noman_land,
            tundra,
            mineral_world
        ]

        #---------------- Binary terrain generation ----------------#
        array = [[VOID for iy in range(height.stop)] for ix in range(length)]
        mem = length * [0]
        mem[0] = headstart
        r = list(range(-deniv, deniv+1))
        turns = 0
        for x in range(1, length):
            same = 0
            for col in mem[:x-1:-1]:
                if col == mem[x]:
                    same += 1
                else:
                    break
    
            new = (not random.randint(0, flatness//same)) * random.choice(r)
            mem[x] = mem[x-1] + new
            while mem[x] not in height:
                if mem[x] < height.start:
                    mem[x] += 1
                else:
                    mem[x] -= 1
    
            if new < 0:
                r = list(range(-deniv, 0)) + [0] * flatness
                turns = flatness
            elif new > 0:
                r = list(range(1, deniv+1)) + [0] * flatness
                turns = flatness
    
            turns -= 1
            if turns == 0:
                r = list(range(-deniv, deniv+1))
    
    
        for x, h in enumerate(mem):
            array[x] = [BLOCK] * h + [VOID] * (len(array[x]) - h)
    
        width = len(array)
        height = len(array[0])
        array = [[array[width-1 - x][y] for x in range(width)][::-1] for y in range(height)][::-1]

        #---------------------- Biomes choice ----------------------#
        biomes = [random.choice(self.liste_biomes) for _ in range(32)]
    
        super().__init__(array)

        #---------------------- Block setting ----------------------#

        new_array = self[:]

        what_can_be_in = lambda depth: [(block if (random.randint(0, 100) in range(block.prob)) and (len(new_array)-depth in block.strat) else STONE) for block in Mineral.blocks]
        distance_from_surface = lambda x, y: len([line[x] for line in self[y::-1] if line[x]])
    
        for y, line in enumerate(new_array):
            for x, block in enumerate(line):
                if block:
                    if distance_from_surface(x, y) > random.randint(3, 5):
                        new_block = random.choice(biomes[self.current_biome]['stone'])
                    elif 0 <= y <= 6 and distance_from_surface(x, y) == 1:
                        new_block = random.choice(biomes[self.current_biome]['snow'])
                    elif distance_from_surface(x, y) == 1:
                        new_block = random.choice(
                            ['Q', 'S', '/§', PASSANT, PASSANT2, PASSANT3, PASSANT4, PASSANT5, PASSANT6,
                             PASSANT7, PASSANT8] + [random.choice(biomes[self.current_biome]['grass'])] * 75)
                    else:
                        new_block = random.choice(biomes[self.current_biome]['dirt'])
                    if y == 19:
                        new_block = INDES

                    #ajout du bloc sélectionné
                    new_array[y][x] = new_block
                else:
                    new_array[y][x] = AIR
                if not x and length > 128:
                    #on est tout à gauche de la map
                    new_array[y][x] = 'p'  #on met de la bedrock

                #on se décale d'un bloc dans le biome
                self.current_biome_size += 1

                if self.current_biome_size >= 128:
                    self.current_biome_size = 0
                    self.current_biome = self.current_biome + 1 if self.current_biome + 1 <= len(biomes) - 1 else 0
    
        for y, line in enumerate(new_array):
            for x, block in enumerate(line):
                if block is STONE:
                    new_array[y][x] = random.choice(what_can_be_in(y))

        super().__init__(new_array)

        #-------------------- Structure setting --------------------#

        new_array = self[:]

        for y, line in enumerate(self):
            for x, block in enumerate(line):
                for s in self.structs:
                    if s.cond(self, (x, y)):
                        self.add_structure(s, (x, y))

    def add_structure(self, struct, pos):
        for block_pos, block in struct.substitute(*pos):
            x, y = block_pos
            if x >= 0 and y >= 0:
                try:
                    self[x, y] = block
                except IndexError:
                    pass

    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            x, y = item
            try:
                return self[y][x]
            except IndexError:
                return None
        else:
            return super().__getitem__(item)

    def __setitem__(self, item, value):
        if isinstance(item, (tuple, list)):
            x, y = item
            try:
                self[y][x] = value
            except IndexError:
                return None
        else:
            super().__setitem__(item, value)

    def __add__(self, other):
        new = self[:]
        for y, line in enumerate(other):
            new[y] += line
        return new


def print_array(array):
    rep = ''
    for line in array:
        for elt in line:
            rep += elt.__repr__()[1:-1]
        rep += '\n'
    print(rep)


if __name__ == '__main__':
    import sys
    valueError = False
    try:
        length, flatness, height = sys.argv[1:4]
        length, flatness, height = map(int, [length, flatness, height])
        headstart, deniv = height//2, 1
        headstart = int(sys.argv[4])
        deniv = int(sys.argv[5])
    except ValueError:
        length, flatness, height, headstart, deniv = 77, 4, 32, 16, 2
        valueError = True
    noise = Map(length, flatness, range(1, height), headstart, deniv)
    if valueError:
        print_array(noise)
        input()