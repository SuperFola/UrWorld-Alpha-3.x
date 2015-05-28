#C:\Python34\python.exe
# -*- coding: utf-8 -*-

from collections import OrderedDict
import os


class Tree(OrderedDict):
    indent = 0
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)
        self.files, self.subdirs = [], []
        subs = os.listdir(self.path)
        tree = {}
        with cd(self.path):
            for path in subs:
                path = '.' + os.sep + path
                if os.access(path, os.X_OK):
                    if os.path.isfile(path):
                        file = File(path)
                        self.files.append(file)
                        tree[file.name] = file
                    else:
                        subdir = Tree(path)
                        self.subdirs.append(subdir)
                        tree[subdir.name] = subdir
            super().__init__(tree)

    def __repr__(self):
        res = ('+-' if not Tree.indent else '-+') + ' {}'.format(self.name)
        Tree.indent += 1
        base_repr = '\n' + ' '.join(['|'] * Tree.indent)
        for subdir in self.subdirs:
            res += base_repr + subdir.__repr__() + '\n' + ('| ' * Tree.indent)
        for file in self.files:
            res += base_repr + '-- ' + file.name
        Tree.indent -= 1
        return res


class File:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.parent = self.path.split(os.sep)[-2]
        self.name = os.path.basename(self.path)
        self.ext = self.name.split('.')[-1]

    def __repr__(self):
        return self.name


class cd:
    def __init__(self, path):
        self.pwd = os.getcwd()
        self.path = path
    def __enter__(self):
        os.chdir(self.path)
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.pwd)