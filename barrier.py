# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:29:09 2019

@author: egor56ru
"""

import pygame
from gameobject import Object
from pygame.time import Clock

class Barrier(Object):
    def __init__(self, image='block', pos=[0, 0], size=None, countdown=None):
        super().__init__(type='barrier')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos
        self.drawn = False
        self.coundown = -countdown if countdown else None
        self.clock = Clock()
        
    def __call__(self, control):
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
        if not self.coundown is None:
            self.coundown += self.clock.tick()
            if self.coundown >= 0:
                control -= self
    
    def destruct(self, control):
        if self.drawn:
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(
                                     self.pos[0],
                                     self.pos[1],
                                     self.size[0],
                                     self.size[1]
                                     ))
        super().destruct(control)
        