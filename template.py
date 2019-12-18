# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Danila Sirotenko
"""

from gameobject import UP, LEFT, DOWN, RIGHT, DIRECTIONS
from dataclasses import dataclass

@dataclass
class Behavior:
    '''
    Template to script for snake. It doesn't work correctly so player should find a mistake and correct it.
    As template shows player can add custom attributes (must be default) and methods (not functions).
    Class name should be "Behavior" and it should contain "run" method which gets 1 argument
    and returns the direction from the list of DIRECTIONS.
    Otherwise game will show an error message.
    
    Шаблон для сценария для змеи. Это не работает правильно, поэтому игрок должен найти ошибку и исправить ее.
    Как показывает шаблон, игрок может добавлять пользовательские атрибуты (должны быть по умолчанию) и методы (не функции).
    Имя класса должно быть «Behavior», и оно должно содержать метод «run», который получает 1 аргумент
    и возвращает направление из списка DIRECTIONS.
    В противном случае игра покажет сообщение об ошибке.
    
    kwargs contains such attributes as:
        direction - current direction
        health - current health
        deaths - number of self deaths
        data - 4 rays that describes what snake see. let ray = data[i], so the format would be:
            ray[0] - direction of ray
            ray[1] - type of object laying on this ray (it can be 'snake', 'self' or 'barrier')
            ray[3] - distance to the object from the head of the snake.
           
           
           kwargs содержит такие атрибуты как:
        направление - текущее направление
        здоровье - текущее здоровье
        смертей - количество смертей
        данные - 4 луча, которые описывают то, что видят змеи. пусть ray = data [i], поэтому формат будет таким:
            луч [0] - направление луча
            луч [1] - тип объекта, лежащего на этом луче (это может быть «змея», «я» или «барьер»)
            луч [3] - расстояние до объекта от головы змеи
    '''
    some_attribute : str = ''
    
    def some_method(self, direction, data):
        new_index = DIRECTIONS.index(direction)
        some_condition = 1
        if not ((data[new_index][1] == 'snake' or data[new_index][1] == 'barrier' or data[new_index][1] == 'self') and data[new_index][2] <= 10):
            return direction
        count = 0
        while count < 7 and some_condition:
            count += 1
            new_index = (DIRECTIONS.index(direction)+1)%4
            direction = DIRECTIONS[new_index]
            some_condition = (data[new_index][1] == 'snake' or data[new_index][1] == 'barrier' or data[new_index][1] == 'self') and data[new_index][2] <= 10
        return direction
    
    def run(self, kwargs):
        '''
        This method defines the way a snake behave.
        Runs every time the snake moves.
        Этот метод определяет движение змеи.
        Работает каждый раз когда змея движется.
        '''
        return self.some_method(kwargs.direction, kwargs.data)
