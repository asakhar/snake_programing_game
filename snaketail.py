# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:29:09 2019

@author: Lizerhigh
"""

import pygame
from gameobject import Object

class SnakeTail(Object):
    def __init__(self, image, pn, pos=[0, 0], size=None):
        super().__init__(type='snake')
        self.img = image.copy()
        self.size = size if size else self.img.get_size()
        self.pos = pos.copy()
        self.drawn = False
        self.parentid = pn
        
    def __eq__(self, a):
        return self.pos == a.pos and self.parentid == a.parentid
        
    def __call__(self, control):
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
    
    def destruct(self, control):
        if self.drawn:    
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(*self.pos, *self.size))
        super().destruct(control)
        