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
        self.piston_collant = 'iii'
        self.receivers = [
            self.cable,
            self.repeteur,
            self.light_on,
            self.light_off,
            self.piston,
            self.piston_collant
        ]
        self.can_ch_states = [
            self.light_off,
            self.light_on,
            self.piston,
            self.piston_collant
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
        self.road_map = []
        for i in self.carte.get_list():
            line = []
            for j in i:
                if j != '0' and j not in self.all:
                    line.append('1')
                else:
                    line.append(j)
            self.road_map.append(line)

    def get_built_tiles(self):
        return self.all

    def put(self, objet, x, y):
        if not self.en_reseau:
            self.road_map[y][x] = objet
        else:
            #en mode réseau, la DED ne fonctionnera pas
            pass

    def put_cable(self, x, y):
        self.carte.remove_bloc(x, y, self.cable)
        self.put(self.cable, x, y)

    def put_interrupt(self, x, y, reverse=False):
        if not reverse:
            tile = self.interrup_off
        else:
            tile = self.interrup_on
        self.carte.remove_bloc(x, y, tile)
        self.put(tile, x, y)

    def put_light(self, x, y, reverse=False):
        if not reverse:
            tile = self.light_off
        else:
            tile = self.light_on
        self.carte.remove_bloc(x, y, tile)
        self.put(tile, x, y)

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
                        pos = (x+i, y)
                    if what_to_do == [-1, 0]:
                        pos = (x-i, y)
                    if what_to_do == [0, +1]:
                        pos = (x, y+i)
                    if what_to_do == [0, -1]:
                        pos = (x, y-i)
                    if self.carte.get_tile(pos[0], pos[1]) in self.receivers and pos not in i_went_through:
                        #on a affaire à un conducteur dedstonique :D
                        #du coup, on le met 'on fire', pour se rappeler qu'il conduit
                        #mais ici, les blocs conduiront la ded ... :/
                        deds_on_fire.append(pos)
                    elif self.carte.get_tile(pos[0], pos[1]) not in self.receivers and pos != (x, y):
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