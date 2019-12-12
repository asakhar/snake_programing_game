# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Danila Sirotenko
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE, K_r, K_n

STAY = [0, 0]
RIGHT = [1, 0]
LEFT = [-1, 0]
UP = [0, -1]
DOWN = [0, 1]
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

WASD = ((UP, K_w), (LEFT, K_a), (DOWN, K_s), (RIGHT, K_d))
ARROWS = ((UP, K_UP), (LEFT, K_LEFT), (DOWN, K_DOWN), (RIGHT, K_RIGHT))

def glob(**kwargs):
    return kwargs

def contra(a, b):
    c = [a[0]+b[0], a[1]+b[1]]
    if (not c[0]) and (not c[1]):
        return True
    return False

class KeyWordArguments:
    def __init__(self, **kwargs):
        self.args = kwargs
        for i in kwargs:
            setattr(self, i, kwargs[i])
            
    def __getitem__(self, key):
        return self.args[key]

class Object:
    def __init__(self, type='object'):
        self.type = type
        
    def __call__(self):
        pass
    
    def destruct(self, control):
        try:
            control.objects.remove(self)
            del self
            #del control.objects[control.objects.index(self)]
        except:
            raise Exception('wtf err')
            