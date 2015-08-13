class DustElectricityDriven:
    def __init__(self, carte, font, surface, en_reseau=False):
        self.stop_conduct_after = 12  # blocks
        self.max_push = 12  # blocks
        self.en_reseau = en_reseau
        self.carte = carte
        self.font = font
        self.ecran = surface
        self.cable = 'ccc'
        self.interrup_off = 'bbb'
        self.interrup_on = 'aaa'
        self.light_off = 'eee'
        self.light_on = 'ddd'
        self.repeteur = 'fff'
        self.piston = 'hhh'
        self.piston_on = 'lll'
        self.piston_collant = 'iii'
        self.piston_collant_on = 'kkk'
        self.receivers = [
            self.cable,
            self.repeteur,
            self.light_on,
            self.light_off,
            self.piston,
            self.piston_collant,
            self.piston_on,
            self.piston_collant_on
        ]
        self.can_ch_states = [
            self.light_off,
            self.light_on,
            self.piston,
            self.piston_collant,
            self.piston_on,
            self.piston_collant_on
        ]
        self.sources = [
            self.interrup_off,
            self.interrup_on
        ]
        self.all = [
            self.cable,
            self.interrup_off,
            self.interrup_on,
            self.light_off,
            self.light_on,
            self.repeteur
        ]

    def get_built_tiles(self):
        return self.all

    def put_cable(self, x, y):
        self.carte.remove_bloc(x, y, self.cable)

    def put_interrupt(self, x, y, reverse=False):
        if not reverse:
            tile = self.interrup_off
        else:
            tile = self.interrup_on
        self.carte.remove_bloc(x, y, tile)

    def use_piston(self, x, y, z, push=True):
        new_x = x + z[0]
        new_y = y + z[1]
        which = 0 if z[0] != 0 else 1
        #on cherche le range dans le lequel on va itérer pour pousser des blocs
        #jusqu'à ce que l'on rencontre du vide
        way = [0, 0]  # default value
        if z[which] == +1:
            #on est dans les x
            if not which:
                way = [0, self.carte.get_x_len() - new_x]
            #on est les y
            else:
                way = [0, self.carte.get_y_len() - new_y]
        if z[which] == -1:
            #on est dans les x
            if not which:
                way = [-new_x, +1]
            #on est dans les y
            else:
                way = [-new_y, 0]
        if push:
            lst = []
            for i in range(way[0], way[1]):
                x2 = new_x + i if not which else new_x
                y2 = new_y + i if which else new_y
                tile = self.carte.get_tile(x2, y2)
                if tile == '0':
                    break
                else:
                    lst.append((x2, y2))
            if len(lst) > self.max_push:
                #trop long, on fait rien dans ce cas
                pass
            else:
                #faut tout décaler :D
                if not which and len(lst) >= 1:
                    #décalage en x
                    if z[which] == +1:
                        #décalage à droite en x
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0]+1, i[1], self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                    if z[which] == -1:
                        #décalage à gauche en x
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0]-1, i[1], self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                if which and len(lst) >= 1:
                    #décalage en y
                    if z[which] == +1:
                        #décalage en bas en y
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0], i[1]+1, self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                    if z[which] == -1:
                        #décalage en haut en y
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0], i[1]-1, self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
            self.carte.remove_bloc(x, y, self.piston_on)
        else:
            self.carte.remove_bloc(new_x, new_y, '0')
            self.carte.remove_bloc(x, y, self.piston)

    def use_piston_collant(self, x, y, z, push=True):
        new_x = x + z[0]
        new_y = y + z[1]
        which = 0 if z[0] != 0 else 1
        #on cherche le range dans le lequel on va itérer pour pousser des blocs
        #jusqu'à ce que l'on rencontre du vide
        way = [0, 0]  # default value
        if z[which] == +1:
            #on est dans les x
            if not which:
                way = [0, self.carte.get_x_len() - new_x]
            #on est les y
            else:
                way = [0, self.carte.get_y_len() - new_y]
        if z[which] == -1:
            #on est dans les x
            if not which:
                way = [-new_x, +1]
            #on est dans les y
            else:
                way = [-new_y, 0]
        if push:
            lst = []
            for i in range(way[0], way[1]):
                x2 = new_x + i if not which else new_x
                y2 = new_y + i if which else new_y
                tile = self.carte.get_tile(x2, y2)
                if tile == '0':
                    break
                else:
                    lst.append((x2, y2))
            if len(lst) > self.max_push:
                #trop long, on fait rien dans ce cas
                pass
            else:
                #faut tout décaler :D
                if not which and len(lst) >= 1:
                    #décalage en x
                    if z[which] == +1:
                        #décalage à droite en x
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0]+1, i[1], self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                    if z[which] == -1:
                        #décalage à gauche en x
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0]-1, i[1], self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                if which and len(lst) >= 1:
                    #décalage en y
                    if z[which] == +1:
                        #décalage en bas en y
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0], i[1]+1, self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
                    if z[which] == -1:
                        #décalage en haut en y
                        for i in lst[::-1]:
                            #on doit prendre la liste à l'envers pour pas effacer de blocs
                            self.carte.remove_bloc(i[0], i[1]-1, self.carte.get_tile(i[0], i[1]))
                        self.carte.remove_bloc(lst[0][0], lst[0][1], '0') #TEMPORAIRE !! sera le self.piston_on apres
            self.carte.remove_bloc(x, y, self.piston_collant_on)
        else:
            self.carte.remove_bloc(new_x, new_y, self.carte.get_tile(new_x + z[0], new_y + z[1]))
            self.carte.remove_bloc(new_x + z[0], new_y + z[1], '0')
            self.carte.remove_bloc(x, y, self.piston_collant)

    def put_light(self, x, y, reverse=False):
        if not reverse:
            tile = self.light_off
        else:
            tile = self.light_on
        self.carte.remove_bloc(x, y, tile)

    def check_all(self, x, y):
        """
        :param x: first position of the click
        :param y: second position of the click
        :return: nothing
        """
        if not self.en_reseau:
            deds_on_fire = []
            i_went_through = []
            what_to_do = []
            for j in range(4):
                #on va choisir la "direction"
                if not j:
                    what_to_do = [+1, 0]
                if j == 1:
                    what_to_do = [-1, 0]
                if j == 2:
                    what_to_do = [0, +1]
                if j == 3:
                    what_to_do = [0, -1]
                for i in range(self.stop_conduct_after):
                    if what_to_do == [+1, 0]:
                        pos = (x+i, y, +1, 0)
                    if what_to_do == [-1, 0]:
                        pos = (x-i, y, -1, 0)
                    if what_to_do == [0, +1]:
                        pos = (x, y+i, 0, +1)
                    if what_to_do == [0, -1]:
                        pos = (x, y-i, 0, -1)
                    if self.carte.get_tile(pos[0], pos[1]) in self.receivers and pos not in i_went_through:
                        #on a affaire à un conducteur dedstonique :D
                        #du coup, on le met 'on fire', pour se rappeler qu'il conduit
                        #mais ici, les blocs conduiront la ded ... :/
                        deds_on_fire.append(pos)
                    elif self.carte.get_tile(pos[0], pos[1]) not in self.receivers and pos[:2] != (x, y):
                        #au cas où c'est le bloc de depart
                        #il n'y a rien pour conduire, on s'arrete la
                        break
                    i_went_through.append(pos)
            for k in deds_on_fire:
                tile = self.carte.get_tile(k[0], k[1])
                if tile in self.can_ch_states:
                    #ce sont des objets pouvant changer d'etat (on/off)
                    if tile == self.light_off:
                        self.put_light(k[0], k[1], reverse=True)
                    if tile == self.light_on:
                        self.put_light(k[0], k[1])
                    if tile == self.piston:
                        self.use_piston(k[0], k[1], k[2:])
                    if tile == self.piston_on:
                        self.use_piston(k[0], k[1], k[2:], push=False)
                    if tile == self.piston_collant:
                        self.use_piston_collant(k[0], k[1], k[2:])
                    if tile == self.piston_collant_on:
                        self.use_piston_collant(k[0], k[1], k[2:], push=False)

    def right_click(self, x, y):
        tile = self.carte.get_tile(x, y)
        if tile in self.all:
            if tile == self.interrup_off:
                self.put_interrupt(x, y, reverse=True)
            if tile == self.interrup_on:
                self.put_interrupt(x, y)
            if tile == self.light_off:
                self.put_light(x, y, reverse=True)
            if tile == self.light_on:
                self.put_light(x, y)
            self.check_all(x, y)