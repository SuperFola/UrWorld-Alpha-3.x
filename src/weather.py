import pygame
from pygame.locals import *
import os
import random
import random as r
import time


class Weather:
    def __init__(self, *methodes):
        self.methodes = methodes

    def update(self):
        for methode in self.methodes:
            methode.update()

    def do(self, action):
        for methode in self.methodes:
            methode.do(action)

    @staticmethod
    def get_action():
        return True


class Wind:
    def __init__(self, carte, ecran, perso):
        self.carte = carte
        self.ecran = ecran
        self.personnage = perso
        self.direction = random.choice(['gauche', 'droite'])
        self.max_pow = 8
        self.power = random.randint(1, self.max_pow)
        self.particules = pygame.image.load(".." + os.sep + "assets" + os.sep + "Particules" + os.sep + "windsand.png").convert_alpha()
        self.can = True
        self.taskdone = False

    def __render(self):
        pass

    def update(self):
        if self.can:
            if self.personnage.get_immobility() > (self.max_pow - self.power) * 3:
                self.personnage.move(self.direction)
            else:
                if not self.taskdone:
                    ratio = self.power if self.personnage.get_direction() == self.direction else -self.power
                    self.personnage.set_speed(self.personnage.get_speed() + ratio)
                    self.taskdone = True
            self.__render()

    def send(self, action):
        if action == 'invert':
            self.can = not self.can
            self.taskdone = False

    def get_action(self):
        return self.can


class Rain:
    def __init__(self, carte, ecran, perso, blocs):
        self.carte = carte
        self.ecran = ecran
        self.personnage = perso
        self.waterflow = True
        self.taskdone = False
        self.rain_falltime = 0
        self.rain_velocity = 2
        self.rain_overlay = pygame.image.load(".." + os.sep + "assets" + os.sep + "Particules" + os.sep + "waterflow.png").convert_alpha()
        self.rain_img = []
        self.blocs = blocs
        pygame.mixer.music.load(".." + os.sep + "assets" + os.sep + "Sons" + os.sep + "6stream.wav")
        self.draw_overlay()

    def draw_overlay(self):
        for i in range(30):
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((76, 76, 76))
            self.surf.set_colorkey((76, 76, 76))

            self.surf.blit(self.rain_overlay, (0, self.rain_falltime - self.rain_overlay.get_height()))
            self.surf.blit(self.rain_overlay, (0, self.rain_falltime))

            self.surf.convert_alpha()

            self.rain_falltime += self.rain_velocity
            self.rain_falltime %= self.rain_overlay.get_height()
            self.rain_img.append(self.surf)
        self.rain_falltime = 0

    def __render(self):
        self.rain_falltime += self.rain_velocity
        for x in range(self.carte.get_space()):
            for y in range(19):
                self.ecran.blit(self.rain_img[self.rain_falltime % len(self.rain_img)], (x * 30, y * 30))

    def update(self):
        if not self.waterflow:
            if not self.taskdone:
                self.personnage.set_speed(self.personnage.get_speed() - 20)
                self.taskdone = True
            pygame.mixer.music.stop()
        if self.waterflow:
            self.__render()
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(".." + os.sep + "assets" + os.sep + "Sons" + os.sep + "6stream.wav")
                pygame.mixer.music.play()

    def toggle_downfalled(self):
        if self.waterflow:
            self.personnage.set_speed(self.personnage.get_speed() + 20)
            self.waterflow = False
        else:
            self.personnage.set_speed(self.personnage.get_speed() - 20)
            self.waterflow = True

    def send(self, action):
        if action == 'toggledownfalled':
            self.toggle_downfalled()

    def get_action(self):
        return self.waterflow


class Storm:
    def __init__(self, carte, ecran, perso):
        self.carte = carte
        self.ecran = ecran
        self.personnage = perso
        self.frequency = 2250
        self.apparition = random.randint(225, self.frequency)
        self.lightning = False
        self.lightner = pygame.image.load(".." + os.sep + "assets" + os.sep + "Particules" + os.sep + "lightning.png").convert_alpha()
        self.pos = (0, 0)
        self.degats_eclair = 15
        self.fall = True

    def __render(self):
        for i in range(0, self.pos[1] // 30 + 1):
            self.ecran.blit(self.lightner, (self.pos[0], i * 30))
        if self.pos[0] - 3 <= self.personnage.get_pos()[0] <= self.pos[0] + 3:
            self.personnage.encaisser_degats(self.degats_eclair / (self.personnage.get_pos()[0] - self.pos[0]) * 0.33)
        time.sleep(0.2)

    def update(self):
        if self.fall:
            self.apparition -= 1
            if not self.apparition:
                x = self.carte.get_fov()[0] + random.randint(0, self.carte.get_space())
                for i in range(0, 20):
                    if self.carte.collide(x, i) and self.carte.get_tile(x, i) != 'p':
                        self.carte.remove_bloc(x, i, '0')
                        self.pos = ((x - self.carte.get_fov()[0]) * 30, i * 30)
                        break
                self.apparition = random.randint(225, self.frequency)
                self.lightning = True
                if self.carte.get_fov()[0] <= x <= self.carte.get_fov()[0] + self.carte.get_space():
                    self.__render()
                self.lightning = False

    def send(self, action):
        pass

    def get_action(self):
        return self.fall


class Clouds:
    def __init__(self, ecran):
        self.ecran = ecran
        self.cloud = pygame.image.load(".." + os.sep + "assets" + os.sep + "Particules" + os.sep + "cloud.png").convert_alpha()
        self.clouds = []
        self.time_to_pop = 0

    def generate(self):
        sens = r.randint(0, 1)
        for i in range(0, r.randint(2, 7)):
            altitude = r.randint(10, 90)
            direction = 1.0 - (altitude / 100 * 1.07)
            direction = direction if sens else -direction
            self.clouds.append([
                [
                    -self.cloud.get_size()[0] if direction > 0 else self.ecran.get_size()[0],
                    altitude
                ],
                direction
            ])

    def draw(self):
        for cloud in self.clouds:
            self.ecran.blit(self.cloud, cloud[0])

    def move_clouds(self):
        if not self.clouds:
            self.generate()
        pop = -1
        for cloud in range(len(self.clouds)):
            self.clouds[cloud][0][0] += self.clouds[cloud][1]
            if self.clouds[cloud][0][0] > self.ecran.get_size()[0]:
                if not self.time_to_pop:
                    self.clouds[cloud][0][0] = -self.cloud.get_size()[0]
                else:
                    pop = cloud
                    self.time_to_pop = 0
            if self.clouds[cloud][0][0] < -self.cloud.get_size()[0]:
                if not self.time_to_pop:
                    self.clouds[cloud][0][0] = self.ecran.get_size()[0]
                else:
                    pop = cloud
                    self.time_to_pop = 0
        if pop != -1:
            self.clouds.pop(pop)

    def update(self):
        self.time_to_pop = r.choice([0] * 15 + [1]) if not self.time_to_pop else 1
        self.move_clouds()
        self.draw()