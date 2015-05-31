class Compressor:
    def __init__(self):
        self.map_len = 4096  # blocks

    def dump(self, object, file):
        compteur = 1
        last = object[0][0]
        tableau = []
        for y, ligne in enumerate(object):
            for x, case in enumerate(ligne):
                if case == last:
                    compteur += 1
                else:
                    tableau.append((compteur, last))
                    compteur = 1
                    last = case
        file.write(str(tableau))
        return True

    def load(self, object):
        compteur = 0
        ligne = 0
        object = exec(object)
        carte = []
        for i in object:
            for x in range(0, i[0] + 1):
                carte[ligne][x] = i[1]
            if compteur != self.map_len:
                compteur += i[0]
            else:
                compteur = 0
                ligne += 1
        return carte