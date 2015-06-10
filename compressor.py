import pickle
import re
from itertools import groupby


class RLECompress:
    def __init__(self, file):
        self.file = file

    def verifier(self, objet):
        if isinstance(objet, list):
            return all(map(lambda elt: isinstance(elt, list), objet))
        return False

    def dump(self, objet):
        temp = list()
        total_element = 0
        if self.verifier(objet):
            for i in objet:
                for j in i:
                    temp.append(j)
                    total_element += 1
            print(total_element)
            total_element = 0
            count = 0
            array = []
            last = temp[0]
            for k in temp:
                if k == last:
                    count += 1
                    total_element += 1
                else:
                    array.append((count, last))
                    last = k
                    count = 1
                    total_element += 1
            print(total_element)
            #self.file.write(str(array))
            pickle.Pickler(self.file).dump(array)


class RLEUncompress:
    def __init__(self, file):
        self.file = file

    def load(self):
        carte_str = pickle.Unpickler(self.file).load()
        temp = []
        temp_element = 0
        for i in carte_str:
            temp += [i[1]] * i[0]
            temp_element += 1 * i[0]
        print(temp_element)
        liste = []
        carte_lst = []
        count = 1
        total_element = 0
        for j in temp:
            if count == 4096:
                count = 1
                carte_lst.append(liste)
                liste = []
            liste.append(j)
            count += 1
            total_element += 1
        print(total_element)
        return carte_lst


RLE_BLOCK_FORMAT = r'\'(\w+)\'(\d+)'


def valid(obj):
    if isinstance(obj, list):
        return all(map(lambda elt: isinstance(elt, list), obj))
    return False


def dump(file, obj):
    group_count = lambda g: len(list(group))
    cpt = 0
    if valid(obj):
        dumped = ''
        for row in obj:
            for tile, group in groupby(row):
                dumped += "'" + tile + "'" + str(group_count(group))
                cpt += int(group_count(group))
            dumped += '\n'
        print(cpt)
        file.write(dumped)
    else:
        raise ValueError("Invalid object format")


def load(file):
    loaded = []
    cpt = 0
    for line in file.readlines():
        row = []
        for tile, count in re.findall(RLE_BLOCK_FORMAT, line):
            row += [tile] * int(count)
            cpt += int(count)
        loaded.append(row)
    print(cpt)
    return loaded