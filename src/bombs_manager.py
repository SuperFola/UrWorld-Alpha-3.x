import time


class BombManager:
    def __init__(self, carte):
        self.carte = carte
        self.boumList = []
        self.bomb = 'cv'

    def add(self, x, y):
        """
        a function who add a bomb to the list
        :param x: position of the block
        :param y: position of the block
        :return: nothing
        """
        self.boumList.append([time.time(), x, y])

    def size(self):
        return len(self.boumList)

    def check(self):
        """
        a function who destroy asynchronicously the bombs
        :return: nothing
        """
        iblist = 0
        while iblist <= len(self.boumList) - 1:
            item = self.boumList[iblist]
            if time.time() - item[0] > 2:
                self.boum_atomique(item[1], item[2])
                self.boumList.pop(iblist)
                self.carte.remove_bloc(item[1], item[2], '0')
            iblist += 1

    def boum_atomique(self, x, y):
        """
        a function who destroy a bomb and some blocs aroud it
        :param x: position of the bomb
        :param y: second position of the bomb
        :return: nothing
        """
        explode_list = [
            (x-3, y),
            (x-2, y),
            (x-1, y),
            (x+1, y),
            (x+2, y),
            (x+3, y),
            (x-1, y-1),
            (x-2, y-1),
            (x, y-1),
            (x+1, y-1),
            (x+2, y-1),
            (x, y-2),
            (x-1, y-2),
            (x+1, y-2),
            (x, y+1),
            (x-1, y+1),
            (x-2, y+1),
            (x-3, y+1),
            (x+1, y+1),
            (x+2, y+1),
            (x+3, y+1),
            (x, y+2),
            (x-1, y+2),
            (x+1, y+2)
        ]

        for i in explode_list:
            if 0 <= i[0] <= self.carte.get_max_fov() and 0 <= i[1] <= self.carte.get_y_len():
                if self.carte.get_tile(i[0], i[1]) != self.bomb and self.carte.get_tile(i[0], i[1]) != 'p':
                    #si il n'y a pas de bombe a coté ni d'eau ni de bedrock
                    self.carte.remove_bloc(i[0], i[1], '0')
                elif self.carte.get_tile(i[0], i[1]) == self.bomb and i != (x, y) and self.carte.get_tile(i[0], i[1]) != "e":
                    #si il y a une bombe à coté
                    self.boumList.append([time.time(), (i[0], i[1])])
                elif self.carte.get_tile(i[0], i[1]) == self.bomb and i[0] == x and i[1] == y:
                    #si j'ai été une bombe à coté d'une autre
                    self.carte.remove_bloc(x, y, '0')