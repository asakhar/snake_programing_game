# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 19:45:50 2019

@author: egor56ru
"""
import pygame
from gameobject import *
from pygame.time import Clock

class Portal(Object):
    '''описание телепорта
        size:   размер, берется из дэфолтного файла, если не не задан другой файл 
        pos:    позиция
        drawn:  отображен ли уже объект
        timer:  время жизни
        clock:  функция из pygame.time, позволяющая отслеживать время жизни
        img:    изображение объекта
        destructbyself: смоуничтожение
        portalid: индекс портала

    '''
    def __init__(self, pos=[0, 0], size=None, countdown=None, portalid=1):
        '''
        задаем начальные значения
        '''
        super().__init__(type='portal')
        self.image = pygame.image.load('images/portal.png')
        self.size = size if size is not None else self.image.get_size()
        self.pos = pos
        self.drawn = False
        self.countdown = countdown
        self.clock = Clock()
        self.clock.tick()
        self.portalid = portalid
        self.destructbyself = False
        
    def __call__(self, control):
        '''
        отрисовка телепорта, с учетом времени его жизни
        '''
        if not self.drawn:
            control.window.blit(self.image, self.pos)
            self.drawn = True
        if self.countdown is not None:
            self.countdown -= self.clock.tick()
            if self.countdown <= 0:
                self.destructbyself = True
                control -= self
        '''
        функционал телепорта
        ищет змейку, которая попала на координаты телепорта, т.е ее коорд совпадает с self.pos
        если нашел то ищет противоположный портал(выход из телепорта)
        передвигает голову на 1 шаг по ходу движения(после выхода)
        потом переносит блок хвоста в место, где голова
        уничтожает телепорты и прошлую змейку
        (противоположные порталы имеют противоположные индексы)
        '''
        snake_tp = control.getbyattr(type='snake', attr='headpos', value=self.pos)#есть ли змейка голова которой на телепорте
        if snake_tp is not None:#если змейка нашлась
            dest_portal = control.getbyattr(type='portal', attr='portalid', value=-self.portalid)#находим противоположный портал(выход)
            snake_tp.headpos = dest_portal.pos.copy()#переносим координаты портала в координаты головы змейки
            snake_tp.headpos = [snake_tp.headpos[0] + snake_tp.direction[0]*10,#
                                snake_tp.headpos[1] + snake_tp.direction[1]*10]#сделать 1 шаг головой, чтобы выйти из портала
            if snake_tp.headpos in control.getproperty(attr='pos'):#случай когда после телепорта голова змейки спавнится в стене
                snake_tp.respawn(control)
            else:
                tail_pos = snake_tp.headpos.copy()#сохраняем позицию головы в переменную 
                snake_tail = control.getbyattr(type='snake', attr='pos', value=self.pos)#находим часть хвоста которая осталась в портале
                snake_tail.pos = tail_pos#переносим хвост в координаты головы
                snake_tail.drawn = False#меняем флаг для перерисовки хвоста
            self.drawn = False#меняем флаг для перерисовки портала
    
    def destruct(self, control):
        '''
        Обновление картинки на экране,
        вместо перерисовки всего изображения измеянем только одну зону
        '''
        if self.drawn and self.destructbyself:
            pygame.draw.rect(control.window, control.bgcolor,
                             pygame.Rect(
                                     self.pos[0],
                                     self.pos[1],
                                     self.size[0],
                                     self.size[1]
                                     ))
        super().destruct(control)