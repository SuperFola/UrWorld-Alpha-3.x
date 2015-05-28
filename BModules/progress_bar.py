# -*- coding: utf-8 -*-
 
import time
import random
import sys
import os
 
os_clear_command = 'cls' if sys.platform == 'win32' else 'clear' # Merci pour le tuyau
"""
class LoadingBar(object):
    def __init__(self, data, max_length):
        self.length = 1
        self.max_length = max_length
        self.data = data
         
    def __repr__(self): return self.data + "\n\n" + "[" + "-" * (self.length-1) + ">" + " " * (self.max_length - self.length) + "]"
	# C'est peu brouillon désolé
     
    def next(self): # Méthode appelée pour que la barre progresse
        if self.length <= self.max_length:
            self.length += 1
     
    def is_not_full(self): # Pas besoin d'expliquer
        return False if self.length == self.max_length else True # Notation cool
"""
class LoadingBar(object):
    def __init__(self, data, max_value, max_length=78):
        self.length = 1
        self.max_value = max_value
        self.max_length = max_length
        self.data = data
        self.amount = lambda: int((((100 * self.length) / self.max_value) / 100) * self.max_length)
     
    def __repr__(self): return "{}\n\n[{}]".format(self.data, ("█" * self.amount()) +  "░" * (self.max_length - self.amount()))
     
    def next(self):
        if self.length <= self.max_value:
            self.length += 1
     
    def is_not_full(self):
        return False if self.length == self.max_value else True