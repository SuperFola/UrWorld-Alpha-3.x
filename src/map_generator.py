import os
import time
import pickle
from gentest import Map


class LaunchMapGen:
    def __init__(self, save_to_file=True):
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
    
    def generer(self, lenght=64, headstart=10):
        print('Début de la génération ...')
        start = time.time()
        if self.save_to_file:
            self.check_for_files()
        else:
            self.check_for_partial_files()
        self.run()
        print('>> %2i minutes %2i secondes.' % (int((time.time() - start) // 60),
                                                int((time.time() - start) % 60)))
        print('Fin de la génération !')
    
    def check_if_exists_and_open(self, path, mode="rb"):
        if os.path.exists(".." + os.sep + "assets" + os.sep + 'Maps' + os.sep + "Settings" + os.sep + path):
            with open(path, mode) as file:
                return pickle.Unpickler(file).load()
        return self.datas[path[:-8:]]
    
    def check_for_files(self):
        for file in self.file_to_load:
            self.datas[file[:-8:]] = self.check_if_exists_and_open(file)

    def check_for_partial_files(self):
        for file in ['height_map.sav', 'flatness_map.sav', 'deniv_map.sav']:
            self.datas[file[:-8:]] = self.check_if_exists_and_open(file)

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
                print(len(map_struct))
                print(len(map_struct[0]))
                with open(".." + os.sep + "assets" + os.sep + "Maps" + os.sep + "map.lvl", "wb") as file:
                    #rle.RLECompress(file).dump(map_struct)
                    pickle.Pickler(file).dump(map_struct)
                    #rle.dump(file, map_struct)
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