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
'''
 модуль, который используется для взаимодействия с игровым времени и его управлением
 функция Clock отвечает за создание объекта, который поможет отслеживать время жизни еды

'''
from random import choice
'''
модуль для генерации случайных чисел, букв, случайного выбора элементов последовательности.
функция choice отвечает за выбор случайного элемента последовательности
'''
class Turtle(Object):
    
    
    '''описание терепашек
        img:    изображение объекта
        size:   размер, берется из дэфолтного файла, если не не задан другой файл 
        pos:    позиция
        drawn:  отображен ли уже объект
        timer:  время жизни
        coundown: обратный отсчет
        clock:  функция из pygame.time, позволяющая отслеживать время жизни
        choices: последовательность из который будет выбираться рандомный элемент
        new_t: новая черепашка
        savepos: сохранение позиции
        coundown: отсчет времени

    '''
    choices = [0, 10, -10]
    
    def __init__(self, image='turtle', pos=[0, 0], size=None, countdown=1000):
        '''
        задаем начальные значения
        '''
        super().__init__(type='barrier')
        self.img = pygame.image.load(f'images/{image}.png')
        self.size = size if size else self.img.get_size()
        self.pos = pos.copy()
        self.drawn = False
        self.coundown = -countdown
        self.clock = Clock()
        
    def __call__(self, control):
        '''
        отрисовка черепашек, с учетом времени их жизни
        '''
        if not self.drawn:
            control.window.blit(self.img, self.pos)
            self.drawn = True
        
        self.coundown += self.clock.tick()
        if self.coundown >= 0:
            savepos = self.pos.copy()
            control -= self
            while 1:
                new_t = Turtle(pos=[
                        savepos[0]+choice(self.choices),
                        savepos[1]+choice(self.choices)
                        ])
                if not (new_t.pos in control.getproperty(attr='pos')):
                    break
            control += new_t
            
    
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
        