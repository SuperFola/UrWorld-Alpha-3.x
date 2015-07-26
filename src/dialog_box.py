import pygame as pg
from pygame.locals import *
import text_entry as txte
import os
import constantes as cst

class DialogBox:
    def __init__(self, surface, texte, titre, center_screen, font, hauteur, type_btn=0, mouse=True, carte=None):
        """
        type = 0 : bouton ok
        type = 1 : bouton oui et bouton non
        type = 2 : texte box et bouton ok
        type = 3 : texte box en mode int et bouton ok

        return 0 pour ok, 1 pour oui et 2 pour non ou bien le resultat de la texte box
        """

        self.cursor = pg.image.load(".." + os.sep + "assets" + os.sep + "Personnage" + os.sep + "Arme" + os.sep + "sword_up_g.png").convert_alpha()
        self.ecran = surface
        self.mouse_aff = mouse
        self.message = texte
        self.titre = titre
        self.type_btn = type_btn if type_btn in (0, 1, 2, 3) else 0
        self.center_screen = [center_screen[0], cst.taille_fenetre_hauteur // 2 - 180]  # center_screen
        self.size = (400, 275)
        self.y_ecart = hauteur
        self.font = font
        self.carte = carte
        self.ok_type0_pos = (self.center_screen[0] - 35 // 2, self.center_screen[1] + self.size[1] // 2 - 38)
        self.oui_type0_pos = (self.center_screen[0] - 35 // 2 - 30, self.center_screen[1] + self.size[1] // 2 - 38)
        self.non_type0_pos = (self.center_screen[0] - 35 // 2 + 30, self.center_screen[1] + self.size[1] // 2 - 38)
        self.text_entry = txte.TextEntry((self.center_screen[0] + 4 - (self.size[0] - 20) // 2, self.center_screen[1] + 40),
                                         self.ecran, size=self.size[0] - 20)
        self.text_entry_int = txte.TextEntry((self.center_screen[0] + 4 - (self.size[0] - 20) // 2, self.center_screen[1] + 40),
                                         self.ecran, size=self.size[0] - 20, type_txt=0)

    def render(self):
        continuer = 1
        btn_ok_focus = False
        btn_oui_focus = False
        btn_non_focus = False

        clicked = 0

        #couleurs
        btn_ok_couleur = (20, 20, 180)
        btn_oui_couleur = (20, 180, 20)
        btn_non_couleur = (180, 20, 20)

        while continuer:
            #le fond
            if self.carte != None:
                self.carte.update()
            else:
                pg.draw.rect(self.ecran, (0, 0, 0), (0, 0, self.ecran.get_size()[0], self.ecran.get_size()[1]))

            #actualisation des couleurs des boutons
            btn_ok_couleur = (20, 20, 180) if not btn_ok_focus else (25, 25, 215)
            btn_oui_couleur = (20, 180, 20) if not btn_oui_focus else (25, 215, 25)
            btn_non_couleur = (180, 20, 20) if not btn_non_focus else (215, 25, 25)

            #fenetre
            pg.draw.rect(self.ecran, (150, 150, 150), (self.center_screen[0] - self.size[0] // 2,
                                                    self.center_screen[1] - self.size[1] // 2,
                                                    self.size[0],
                                                    self.size[1]))
            #"barre" de titre
            pg.draw.rect(self.ecran, (60, 60, 60), (self.center_screen[0] - self.size[0] // 2,
                                                    self.center_screen[1] - self.size[1] // 2,
                                                    self.size[0],
                                                    30))
            #message
            if type(self.message) == str:
                message = self.font.render(self.message, 1, (10, 10, 10))
                self.ecran.blit(message,
                                (self.center_screen[0] + 10 - message.get_size()[0] // 2,
                                self.center_screen[1] - self.size[1] // 2 + 50))
            elif type(self.message) == list:
                message = self.font.render(self.message[0], 1, (10, 10, 10))
                message2 = None
                self.ecran.blit(message,
                                (self.center_screen[0] + 10 - message.get_size()[0] // 2,
                                self.center_screen[1] - self.size[1] // 2 + 50))
                if len(self.message) >= 2:
                    message2 = self.font.render(self.message[1], 1, (10, 10, 10))
                    self.ecran.blit(message2,
                                    (self.center_screen[0] + 10 - message.get_size()[0] // 2,
                                    self.center_screen[1] - self.size[1] // 2 + 50 + message.get_size()[1]))
                if len(self.message) >= 3:
                    message3 = self.font.render(self.message[2], 1, (10, 10, 10))
                    self.ecran.blit(message3,
                                    (self.center_screen[0] + 10 - message.get_size()[0] // 2,
                                    self.center_screen[1] - self.size[1] // 2 + 50 + message.get_size()[1] + message2.get_size()[1] + 10))
            #titre
            titre = self.font.render(self.titre, 1, (10, 10, 10))
            self.ecran.blit(titre,
                            (self.center_screen[0] + 10 - titre.get_size()[0] // 2,
                            self.center_screen[1] - self.size[1] // 2 + 2))
            #boutons
            if self.type_btn == 0 or self.type_btn == 2 or self.type_btn == 3:
                ok = self.font.render('Ok', 1, (10, 10, 10))
                pg.draw.rect(self.ecran, btn_ok_couleur, (self.ok_type0_pos[0],
                                                         self.ok_type0_pos[1],
                                                        35,
                                                        30))
                self.ecran.blit(ok, (self.center_screen[0] + 2 - ok.get_size()[0] // 2,
                                     self.center_screen[1] + self.size[1] // 2 - 36))
            elif self.type_btn == 1:
                oui = self.font.render('Oui', 1, (10, 10, 10))
                non = self.font.render('Non', 1, (10, 10, 10))
                pg.draw.rect(self.ecran, btn_oui_couleur, (self.oui_type0_pos[0],
                                                        self.oui_type0_pos[1],
                                                        40,
                                                        30))
                pg.draw.rect(self.ecran, btn_non_couleur, (self.non_type0_pos[0],
                                                        self.non_type0_pos[1],
                                                        40,
                                                        30))
                self.ecran.blit(oui, (self.center_screen[0] + 2 - oui.get_size()[0] // 2 - 30,
                                    self.center_screen[1] + self.size[1] // 2 - 36))
                self.ecran.blit(non, (self.center_screen[0] + 2 - non.get_size()[0] // 2 + 31,
                                    self.center_screen[1] + self.size[1] // 2 - 36))

            #event
            for e in pg.event.get():
                if e.type == MOUSEBUTTONUP:
                    if self.type_btn == 0 or self.type_btn == 2 or self.type_btn == 3:
                        if self.ok_type0_pos[0] <= e.pos[0] <= self.ok_type0_pos[0] + 35 \
                                and self.ok_type0_pos[1] + self.y_ecart <= e.pos[1] <= self.ok_type0_pos[1] + 30 + self.y_ecart:
                            continuer = 0
                    elif self.type_btn == 1:
                        if self.oui_type0_pos[0] <= e.pos[0] <= self.oui_type0_pos[0] + 40 \
                            and self.oui_type0_pos[1] + self.y_ecart <= e.pos[1] <= self.oui_type0_pos[1] + 30 + self.y_ecart:
                            clicked = 1
                            continuer = 0
                        elif self.non_type0_pos[0] <= e.pos[0] <= self.non_type0_pos[0] + 40 \
                            and self.non_type0_pos[1] + self.y_ecart <= e.pos[1] <= self.non_type0_pos[1] + 30 + self.y_ecart:
                            clicked = 2
                            continuer = 0
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        continuer = 0
                    else:
                        if self.type_btn == 2:
                            self.text_entry.add_letter(e)
                        elif self.type_btn == 3:
                            self.text_entry_int.add_letter(e)

            #le focus
            x_s, y_s = pg.mouse.get_pos()
            if self.mouse_aff:
                self.ecran.blit(self.cursor, (x_s, y_s - self.y_ecart))
            if self.type_btn == 0:
                if self.ok_type0_pos[0] <= x_s <= self.ok_type0_pos[0] + 35 \
                    and self.ok_type0_pos[1] + self.y_ecart <= y_s <= self.ok_type0_pos[1] + 30 + self.y_ecart:
                    btn_ok_focus = True
                else:
                    btn_ok_focus = False
            elif self.type_btn == 1:
                if self.oui_type0_pos[0] <= x_s <= self.oui_type0_pos[0] + 40 \
                    and self.oui_type0_pos[1] + self.y_ecart <= y_s <= self.oui_type0_pos[1] + 30 + self.y_ecart:
                    btn_oui_focus = True
                else:
                    btn_oui_focus = False
                if self.non_type0_pos[0] <= x_s <= self.non_type0_pos[0] + 40 \
                    and self.non_type0_pos[1] + self.y_ecart <= y_s <= self.non_type0_pos[1] + 30 + self.y_ecart:
                    btn_non_focus = True
                else:
                    btn_non_focus = False
            elif self.type_btn == 2:
                self.text_entry.render()

                if self.ok_type0_pos[0] <= x_s <= self.ok_type0_pos[0] + 35 \
                    and self.ok_type0_pos[1] + self.y_ecart <= y_s <= self.ok_type0_pos[1] + 30 + self.y_ecart:
                    btn_ok_focus = True
                else:
                    btn_ok_focus = False
            elif self.type_btn == 3:
                self.text_entry_int.render()

                if self.ok_type0_pos[0] <= x_s <= self.ok_type0_pos[0] + 35 \
                    and self.ok_type0_pos[1] + self.y_ecart <= y_s <= self.ok_type0_pos[1] + 30 + self.y_ecart:
                    btn_ok_focus = True
                else:
                    btn_ok_focus = False

            #actualisation de l'ecran
            pg.display.flip()

        if self.type_btn == 2:
            clicked = self.text_entry.value()
        elif self.type_btn == 3:
            clicked = self.text_entry_int.value()

        if self.type_btn != 0:
            return clicked