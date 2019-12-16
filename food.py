# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:11:20 2019

@author: egor56ru
"""
import pygame
'''
библиотека для создания игр
'''
from gameobject import Object
'''
gameobject представляет собой визуальный объект,
знающий о том, как себя рендерить, сохранять свои границы и перемещаться
'''
from pygame.time import Clock
'''
 модуль, который используется для взаимодействия с игровым времени и его управлением
'''

class Food(Object):
    '''описание еды
        size:   размер, берется из дэфолтного файла, если не не задан другой файл 
        pos:    позиция
        drawn:  отображен ли уже объект
        timer:  время жизни
        clock:  функция из pygame.time, позволяющая отслеживать время жизни
        img:    изображение объекта

    '''
    def __init__(self, image='food', pos=[0, 0], size=None):
        '''
        задаем начальные значения
        '''
        super().__init__(type='food')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos.copy()
        self.drawn = False
        self.timer = -10000
        self.clock = Clock()
        
    def __call__(self, control):
        '''
        отрисовка еды, с учетом времени её жизни
        '''
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
        if self.timer>=0:
            control -= self
        self.timer += self.clock.tick()
    
    def destruct(self, control):
        '''
        Обновление картинки на экране,
        вместо перерисовки всего изображения измеянем только одну зону
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
        