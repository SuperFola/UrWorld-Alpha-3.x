import pygame
import math
import os


class Skybox:
    def __init__(self, screen, color):
        self.screen = screen
        self.ratio = self.screen.get_size()[1] - 35
        self.difference_y = self.screen.get_size()[1] - self.ratio
        self.width = self.screen.get_size()[0]
        self.height = self.screen.get_size()[1]
        self.count = 0
        self.limite_frame = 1000
        self.pos = (0, 0)
        self.max_color = 200
        self.game_time = 0
        self.max_game_time = 23
        self.color = list(color)
        self.img_bad_weather = pygame.Surface(self.screen.get_size())
        self.img_bad_weather.fill((76, 76, 76))
        self.img_bad_weather.fill(self.color)
        self.skybox = []
        self.min = 0
        self.had_bad_weather = False
        self.font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 8)
        self.generate()

    def get_max_time_game(self):
        return self.max_game_time

    def get_clock(self):
        surf = pygame.Surface((30, 30))
        frequency = 0.3
        i = self.min // 3.25
        red = math.sin(frequency * i + 0) * 127 + 128
        green = math.sin(frequency * i + 2 * math.pi / 3) * 127 + 128
        blue = math.sin(frequency * i + 4 * math.pi / 3) * 127 + 128
        surf.fill((red, green, blue))
        txt = self.font.render(self.get_s_prtime(), 1, (10, 10, 10))
        surf.blit(txt, ((30 - txt.get_size()[0]) // 2, (30 - txt.get_size()[1]) // 2))
        return surf

    def get_game_time(self):
        return self.game_time

    def get_s_prtime(self):
        return str(self.game_time) + ":" + str(self.min)

    def get_bad_weather(self):
        return self.had_bad_weather

    def get_color(self):
        return self.skybox[self.game_time][1]

    def change_color(self, color):
        self.color = color
        self.generate()

    def bad_weather(self, boolean):
        self.had_bad_weather = boolean

    def generate(self):
        #cela va prendre pas mal de temps, donc à lancer une seule fois !
        #et au démarrage du jeu si possible :D
        for i in range(1, self.max_game_time + 1):
            img = pygame.Surface(self.screen.get_size())
            copie_color = self.color[:]
            copie_color = [k - i * 2 for k in copie_color]
            last_color = copie_color
            #on vérifie qu'il n'y a pas de couleurs négatives
            for k in range(len(copie_color)):
                if copie_color[k] < 0:
                    copie_color[k] = 0
            #on colore et on ajoute l'horizon
            img.fill(tuple(copie_color))
            pygame.draw.rect(img, (64, 64, 64), (0, self.ratio, self.width, self.difference_y))
            #on ajoute cette partie de skybox a la liste d'images
            self.skybox.append([img, last_color])
        #image bad weather
        pygame.draw.rect(self.img_bad_weather, (64, 64, 64), (0, self.ratio, self.width, self.difference_y))

    def draw(self):
        if not self.had_bad_weather:
            self.screen.blit(self.skybox[self.game_time][0], self.pos)
        else:
            self.screen.blit(self.img_bad_weather, self.pos)
        self.update_time()

    def update_time(self):
        self.count += 1
        if self.count >= self.limite_frame:
            self.count = 0
            self.game_time += 1
            if self.game_time == self.max_game_time:
                self.game_time = 0
            self.min = 0
        self.min = self.count // 8