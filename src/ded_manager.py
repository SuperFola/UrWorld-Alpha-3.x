class DustElectricityDriven:
    def __init__(self, carte, font, surface, en_reseau=False):
        self.stop_conduct_after = 12  # blocks
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
        way = [0, 0]  #default value
        if z[which] == +1:
            #on est dans les x
            if not which:
                way = [new_x, self.carte.get_x_len()]
            #on est les y
            else:
                way = [new_y, self.carte.get_y_len()]
        if z[which] == -1:
            #on est dans les x
            if not which:
                way = [-new_x, +1]
            #on est dans les y
            else:
                way = [-new_y, +1]
        if push:
            for i in range(way[0], way[1]):
                cur_pos = (i, new_y) if not which else (new_x, i)
                next_one = (i + z[which], new_y) if not which else (new_x, i + z[which])
                if self.carte.get_tile(next_one[0], next_one[1]) == '0':
                    break
                else:
                    self.carte.remove_bloc(next_one[0], next_one[1], self.carte.get_tile(cur_pos[0], cur_pos[1]))
        else:
            self.carte.remove(new_x, new_y, '0')

    def use_piston_collant(self, x, y, z, push=True):
        new_x = x + z[0]
        new_y = y + z[1]
        which = 0 if z[0] != 0 else 1
        #on cherche le range dans le lequel on va itérer pour pousser des blocs
        #jusqu'à ce que l'on rencontre du vide
        way = [0, 0]  #default value
        if z[which] == +1:
            #on est dans les x
            if not which:
                way = [new_x, self.carte.get_x_len()]
            #on est les y
            else:
                way = [new_y, self.carte.get_y_len()]
        if z[which] == -1:
            #on est dans les x
            if not which:
                way = [-new_x, +1]
            #on est dans les y
            else:
                way = [-new_y, +1]
        if push:
            for i in range(way[0], way[1]):
                cur_pos = (i, new_y) if not which else (new_x, i)
                next_one = (i + z[which], new_y) if not which else (new_x, i + z[which])
                if self.carte.get_tile(next_one[0], next_one[1]) == '0':
                    break
                else:
                    self.carte.remove_bloc(next_one[0], next_one[1], self.carte.get_tile(cur_pos[0], cur_pos[1]))
        else:
            self.carte.remove_bloc(new_x, new_y, self.carte.get_tile(new_x + z[0], new_y + z[1]))

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