import pygame
from pygame.locals import *
import os

pygame.font.init()


class TextEntry:
    def __init__(self, position, surface, size=194, type_txt='', default_value=''):
        self.texte = default_value
        self.size = size
        self.max_len = self.size // 11
        self.pos = position
        self.next_to_upper = False
        self.surface = surface
        self.focus = True
        self.type_txt = type_txt
        self.dict_special = [
            K_LSHIFT,
            K_RSHIFT,
            K_BACKSPACE,
            K_CAPSLOCK,
            K_NUMLOCK,
            K_MENU,
            K_MODE,
            K_PAUSE,
            K_POWER,
            K_UNDERSCORE,
            K_HASH,
            K_LEFT,
            K_UP,
            K_RIGHT,
            K_DOWN,
            K_LALT,
            K_RALT,
            K_LCTRL,
            K_RCTRL,
            K_LSUPER,
            K_RSUPER,
            K_RMETA,
            K_LMETA,
            K_HELP,
            K_HOME,
            K_END,
            K_INSERT,
            K_PRINT,
            K_PAGEUP,
            K_PAGEDOWN,
            K_FIRST,
            K_LAST,
            K_F1,
            K_F2,
            K_F3,
            K_F4,
            K_F5,
            K_F6,
            K_F7,
            K_F8,
            K_F9,
            K_F10,
            K_F11,
            K_F12,
            K_F13,
            K_F14,
            K_F15,
            K_TAB,
            K_RETURN,
            K_SCROLLOCK,
            K_SYSREQ,
            K_BREAK,
            K_DELETE,
            K_CLEAR
        ]
        self.dict_autorise = ['all']
        if type(self.type_txt) == int:
            self.dict_autorise = [
                K_KP0,
                K_KP1,
                K_KP2,
                K_KP3,
                K_KP4,
                K_KP5,
                K_KP6,
                K_KP7,
                K_KP8,
                K_KP9,
                K_0,
                K_1,
                K_2,
                K_3,
                K_4,
                K_5,
                K_6,
                K_7,
                K_8,
                K_9
            ]
            self.max_len = 2
        self.font = pygame.font.Font(".." + os.sep + "assets" + os.sep + "GUI" + os.sep + "Fonts" + os.sep + "freesansbold.otf", 10)

    def render(self):
        pygame.draw.rect(self.surface, (10, 10, 10), (self.pos[0] - 4, self.pos[1] - 4, self.size + 4, 28))
        pygame.draw.rect(self.surface, (180, 180, 180), (self.pos[0] - 2, self.pos[1] - 2, self.size, 24))
        self.surface.blit(self.font.render(str(self.texte), 1, (10, 10, 10)), self.pos)

    def add_letter(self, key_pg):
        impossible = False
        if self.focus:
            if key_pg.key not in self.dict_special:
                key_pg = ord(key_pg.dict['unicode'])
            elif type(self.type_txt) == int and key_pg.key not in self.dict_autorise:
                impossible = True
                key_pg = key_pg.key
            else:
                impossible = True
                key_pg = key_pg.key
            if not impossible:
                if 32 <= int(key_pg.__str__()) <= 128 and len(self.texte) + 1 <= self.max_len:
                    if self.next_to_upper:
                        self.texte += chr(key_pg).capitalize()
                    else:
                        self.texte += chr(key_pg)
                    self.next_to_upper = False
            else:
                if key_pg == K_RSHIFT or key_pg == K_LSHIFT:
                    self.upper()
                if key_pg == K_BACKSPACE:
                    self.texte = self.texte[:len(self.texte)-1:]

    def upper(self):
        self.next_to_upper = True

    def value(self):
        return self.texte

    def get_focus(self):
        return self.focus

    def set_focus(self, new_focus):
        self.focus = new_focus