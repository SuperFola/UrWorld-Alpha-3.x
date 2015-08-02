import pygame


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
        self.had_bad_weather = False
        self.generate()

    def get_max_time_game(self):
        return self.max_game_time

    def get_game_time(self):
        return self.game_time

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