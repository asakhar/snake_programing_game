# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:11:20 2019

@author: EMoldovsky
"""
import pygame
from gameobject import Object
from pygame.time import Clock

class Slowdown(Object):
    '''
    Класс для объектов типа "замедлялка"
    Конструктор
        slowdown : str - название изобращения для объекта
        pos : List[2] - позиция на сцене
        size : Tuple[2]|None - размер текстурки
    '''
    
    def __init__(self, image='slowdown', pos=[0, 0], size=None):
        '''Конструктор'''
        super().__init__(type='slowdown')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos.copy()
        self.drawn = False
        self.timer = -10000
        self.clock = Clock()
        
    def __call__(self, control):
        '''Отрисовка и обратный отсчет'''
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
        if self.timer>=0:
            control -= self
        self.timer += self.clock.tick()
    
    def destruct(self, control):
        '''Удаление со сцены'''
        if self.drawn:
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(
                                     self.pos[0],
                                     self.pos[1],
                                     self.size[0],
                                     self.size[1]
                                     ))
        super().destruct(control)
        