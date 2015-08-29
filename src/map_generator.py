import os
import time
import glob
import pickle
from gentest import Map
from copy import deepcopy


class LaunchMapGen:
    def __init__(self, save_to_file=True, chunks_gen=False):
        self.file_to_load = [
            'height_map.sav',
            'flatness_map.sav',
            'deniv_map.sav',
            'headstart_map.sav',
            'lenght_map.sav',
        ]
        self.datas = {
            'lenght': 4096,
            'flatness': 4,
            'height': 20,
            'headstart': 10,
            'deniv': 1
        }
        self.save_to_file = save_to_file
        self.chunks_gen = chunks_gen
        self.save_dir = ".." + os.sep + "assets" + os.sep + "Maps" + os.sep

    def generer(self, lenght=64, headstart=10, chunk_size=64):
        print('Début de la génération ...')
        start = time.time()
        chunk = None
        if self.save_to_file:
            self.check_for_files()
        else:
            self.check_for_partial_files()
        if not self.chunks_gen:
            chunk = self.run()
        else:
            chunk = self.run_to_chunk(lenght, headstart, chunk_size)
        print('>> %2i minutes %2i secondes.' % (int((time.time() - start) // 60),
                                                int((time.time() - start) % 60)))
        print('Fin de la génération !')
        if chunk:
            return chunk
    
    def check_if_exists_and_open(self, path, mode="rb"):
        if os.path.exists(self.save_dir + "Settings" + os.sep + path):
            with open(self.save_dir + "Settings" + os.sep + path, mode) as file:
                return pickle.Unpickler(file).load()
        return self.datas[path[:-8:]]

    def check_for_files(self):
        for file in self.file_to_load:
            self.datas[file[:-8:]] = self.check_if_exists_and_open(file)

    def check_for_partial_files(self):
        for file in ['height_map.sav', 'flatness_map.sav', 'deniv_map.sav']:
            self.datas[file[:-8:]] = self.check_if_exists_and_open(file)

    def get_height(self, x, carte):
        height = self.datas['height']
        for y in range(0, self.datas['height']):
            if carte[y][x] in ('hhh', 'iii', 'eee', 'bbb', 'ccc', 'fff', 'ggg', 's', 'h', 'U', 'I', 'az', 'ze', 'd'):
                height = self.datas['height'] - y
                break
        return height

    def run_to_chunk(self, lenght, headstart, chunk_size):
        map_struct = list(Map(lenght,
                          self.datas['flatness'],
                          range(1, self.datas['height']),
                          headstart,
                          self.datas['deniv'],
                          chunk_size=chunk_size))
        for y in range(len(map_struct)):
            for x in range(len(map_struct[0])):
                map_struct[y][x] = str(map_struct[y][x])
        if not self.save_to_file:
            return map_struct
        else:
            with open(self.save_dir + "chunk" + str(len(glob.glob(self.save_dir + "*.chk"))) + ".chk", "wb") as file:
                #rle.RLECompress(file).dump(map_struct)
                pickle.Pickler(file).dump(map_struct)
                #rle.dump(file, map_struct)
            return self.get_height(len(map_struct) - 1, map_struct)

    def run(self):
        if self.save_to_file:
            if not os.path.exists(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl"):
                map_struct = list(Map(self.datas["lenght"],
                                      self.datas['flatness'],
                                      range(1, self.datas['height']),
                                      self.datas['headstart'],
                                      self.datas['deniv']))
                for y, ligne in enumerate(map_struct):
                    for x, elem in enumerate(ligne):
                        map_struct[y][x] = str(map_struct[y][x])
                with open(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl", "wb") as file:
                    #rle.RLECompress(file).dump(map_struct)
                    pickle.Pickler(file).dump([map_struct, deepcopy(map_struct)])
                    #rle.dump(file, map_struct)
                return None
        else:
            map_struct = list(Map(self.datas["lenght"],
                                  self.datas['flatness'],
                                  range(1, self.datas['height']),
                                  self.datas['headstart'],
                                  self.datas['deniv']))
            for y, ligne in enumerate(map_struct):
                for x, elem in enumerate(ligne):
                    map_struct[y][x] = str(map_struct[y][x])
            return map_struct