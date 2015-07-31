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
        aim of the funciton : check all the DED's elements and turn them on or off
        nodes: if we reach a node, we add it to this list, with the position, the intensity of the DED,
            and the way already used at this node
        paths: path[0] contains [start point, end point, way, intensity of the DED at the end of the path
        way: can take the values :
            0: up
            1: right
            2: down
            3: left
        cur_intensity: current intensity of the DED in the current iteration
        :param x: first position of the click
        :param y: second position of the click
        :return: nothing
        """
        if not self.en_reseau:
            nodes = []
            paths = []
            way = 0
            cur_intensity = self.stop_conduct_after


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