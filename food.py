# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:11:20 2019

@author: egor56ru
"""
import pygame
from gameobject import Object
from pygame.time import Clock

class Food(Object):
    def __init__(self, image='food', pos=[0, 0], size=None):
        super().__init__(type='food')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos.copy()
        self.drawn = False
        self.timer = -10000
        self.clock = Clock()
        
    def __call__(self, control):
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
        if self.timer>=0:
            control -= self
        self.timer += self.clock.tick()
    
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
        