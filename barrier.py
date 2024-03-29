# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:29:09 2019

@author: egor56ru
"""

import pygame
'''
библиотека для создания игр
'''
from gameobject import Object
'''
берем класс Object из файла gameobject представляющий собой визуальный объект
'''
from pygame.time import Clock

class Barrier(Object):
    '''описание барьера
        size:   размер, берется из дэфолтного файла, если не не задан другой файл 
        pos:    позиция
        drawn:  отображен ли уже объект
        timer:  время жизни
        clock:  функция из pygame.time, позволяющая отслеживать время жизни
        img:    изображение объекта

    '''
    def __init__(self, image, pos=[0, 0], size=None, countdown=None):
        '''
        задаем начальные значения
        '''
        super().__init__(type='barrier')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos
        self.drawn = False
        self.countdown = -countdown if countdown else None
        self.clock = Clock()
        
    def __call__(self, control):
        if not self.countdown is None:
            self.countdown += self.clock.tick()
            if self.countdown >= 0:
                control -= self
        '''
        отрисовка барьера
        '''
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
    
    def destruct(self, control):
        '''
        Обновление картинки на экране,
        вместо перерисовки всего изображения изменяем только одну зону
        '''
        if self.drawn:
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(
                                     self.pos[0],
                                     self.pos[1],
                                     self.size[0],
                                     self.size[1]
                                     ))
        super().destruct(control)
        
