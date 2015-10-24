import os
import pygame


class Fluides:
    def __init__(self, ecran, carte):
        self.ecran = ecran
        self.carte = carte
        self._img = []
        self._img2 = []
        self.velocity = 1
        self.time = 0
        self.image = None
        self.imagenrmlt = None
        self.tile_code = ''

    def draw_overlay(self):
        for i in range(int(30 // self.velocity)):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.image, (self.time - self.image.get_width(), 0))
            self.surf.blit(self.image, (self.time, 0))

            self.surf.convert_alpha()

            self.time += self.velocity
            self.time %= self.image.get_width()
            self._img.append(self.surf)

        self.time = 0

        for i in range(int(30 // self.velocity)):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.imagenrmlt, (self.time - self.imagenrmlt.get_width(), 0))
            self.surf.blit(self.imagenrmlt, (self.time, 0))

            self.surf.convert_alpha()

            self.time += self.velocity
            self.time %= self.imagenrmlt.get_width()
            self._img2.append(self.surf)
        self.time = 0

    def draw(self):
        self.time += self.velocity
        crt = self.carte.get_map_fov()
        for y in range(len(crt)):
            for x in range(len(crt[y])):
                if y - 1 >= 0:
                    if crt[y-1][x] == self.tile_code and crt[y][x] == self.tile_code:
                        self.ecran.blit(self._img2[int(self.time % len(self._img))], (x * 30, y * 30))
                    elif crt[y-1][x] != self.tile_code and crt[y][x] == self.tile_code:
                        self.ecran.blit(self._img[int(self.time % len(self._img2))], (x * 30, y * 30))
                else:
                    if crt[y][x] == self.tile_code:
                        self.ecran.blit(self._img[int(self.time % len(self._img2))], (x * 30, y * 30))

    def update(self):
        self.draw()


class Water(Fluides):
    def __init__(self, ecran, carte):
        super().__init__(ecran, carte)
        self.image = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "eaumvt.png").convert_alpha()
        self.imagenrmlt = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "eau.png").convert_alpha()
        self.tile_code = 'e'
        self.velocity = 0.5
        self.draw_overlay()


class Lava(Fluides):
    def __init__(self, ecran, carte):
        super().__init__(ecran, carte)
        self.image = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "lavamvt.png").convert_alpha()
        self.imagenrmlt = pygame.image.load(".." + os.sep + "assets" + os.sep + "Tiles" + os.sep + "lava.png").convert_alpha()
        self.tile_code = 'lav'
        self.velocity = 0.5
        self.draw_overlay()

    def fire_blocks(self):
        crt = self.carte.get_map_fov()
        for y in range(len(crt)):
            for x in range(len(crt[y])):
                if crt[y][x] == self.tile_code:
                    if x - 1 >= 0:
                        if crt[y][x-1] in self.carte.get_fire_list():
                            self.carte.fire_bloc(self.carte.get_first_fov() + x-1, y)
                    if x + 1 < len(crt[0]):
                        if crt[y][x+1] in self.carte.get_fire_list():
                            self.carte.fire_bloc(self.carte.get_first_fov() + x+1, y)
                    if y - 1 >= 0:
                        if crt[y-1][x] in self.carte.get_fire_list():
                            self.carte.fire_bloc(self.carte.get_first_fov() + x, y-1)
                    if y + 1 < len(crt):
                        if crt[y+1][x] in self.carte.get_fire_list():
                            self.carte.fire_bloc(self.carte.get_first_fov() + x, y+1)

    def update(self):
        self.draw()
        self.fire_blocks()