# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:11:20 2019

@author: Valeria Domanova
"""
import pygame
from gameobject import Object
from pygame.time import Clock

class MegaFood(Object):
    '''Implements the object class which is responsible for MegaFood'''
    
    def __init__(self, image='megafood', pos=[0, 0], size=None):
        super().__init__(type='food')
        '''characteristic of object'''
        self.img = pygame.image.load(f'images/{image}.png') #graphical representation of the object
        self.size = size if size else self.img.get_size() #size of object
        self.pos = pos.copy() #position of the object
        self.drawn = False #is the object displayed
        self.timer = -2000 #lifetime of the object
        self.clock = Clock() #tracking the lifetime of the object
        self.mega = True #is the object "mega" 
        
    def __call__(self, control):
        '''If there is no object in the scene, the function creates it.
        If there is an object in the scene, the function counts the time of its existence'''
        #if the object is missing create it
        if not self.drawn: 
            control.window.blit(self.img, self.pos)
            self.drawn = True
        # if an object is present consider its lifetime
        if self.timer>=0:
            control -= self
        self.timer += self.clock.tick()
    
    def destruct(self, control):
        '''When the lifetime of an object is out the function destroys it.'''
        if self.drawn:
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(
                                     self.pos[0],
                                     self.pos[1],
                                     self.size[0],
                                     self.size[1]
                                     ))
        super().destruct(control)
        
