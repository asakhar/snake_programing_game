# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Danila Sirotenko
"""
"""
Basic class for all subjects of scene are defined by method "dystract", which responsibles for deleting object from scene and mashing texture behind him,
he has atribute "type", which is the type name of this object.
Базовый класс для всех объектов сцены,для него определен метод "destract" ,который отвечает за удаление объекта со сцены и затирания за ним текстуры,
он имеет атрибут "type", который представляет собой название типа этого объекта.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE, K_r, K_n

STAY = [0, 0]
RIGHT = [1, 0]
LEFT = [-1, 0]
UP = [0, -1]
DOWN = [0, 1]
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]
"""
Inplenmenting moves on the coordinate flatness.
Осуществление движения на координатной плоскости.
"""

WASD = ((UP, K_w), (LEFT, K_a), (DOWN, K_s), (RIGHT, K_d))
"""
Constant for controller ,for managing from keyboard how they move,i.e. that means direction and button which responses for this ( her code).
Константа для контроллера,для управления с клавиатуры,как они движутся,т.е. направление и кнопка которая за это отвечает(её код).
"""
ARROWS = ((UP, K_UP), (LEFT, K_LEFT), (DOWN, K_DOWN), (RIGHT, K_RIGHT))
"""
Same thing only for arrows.
Тоже самое только для стрелочек.
"""

def contra(a, b):
     """
A function for determining whether the directions A and B are opposite, i.e. if the directions are opposite, are current and selected, then he does not use them,
because the snake will eat itself.
Функция для определения являются ли направления А и Б противоположными,т.е. если направления противоположны,текущее и выбранное ,то он их не использует,
потому что змейка сама себя тогда съест.
    """
    c = [a[0]+b[0], a[1]+b[1]]
    if (not c[0]) and (not c[1]):
        return True
    return False

class KeyWordArguments:
    """
The class that is used in snakescript1 in the def run function, the arguments of this class are passed to it to make it more convenient to get: "kwargs.data",
just a convenient call argument from this class.
Класс который используется в snakescript1 в функцию def run,в него передаются аргументы из этого класса,для того чтобы их можно было удобнее извлекать:"kwargs.data",
просто удобный вызов аргумента из этого класса. 
"""
    def __init__(self, **kwargs):#**kwargs - именнованные аргументы,с которыми можно работать ,как со словарем. 
        self.args = kwargs
        for i in kwargs:
            """
            Для того чтобы извлечь аргумент через точку.
            """
            setattr(self, i, kwargs[i])
            
    def __getitem__(self, key):
        return self.args[key]
"""
To get an argument through square brackets and quotation marks.
Чтобы получить аргумента через квадратные скобки и ковычки.
"""
class Object:
    """
The base class, which is any object on the stage, has a constructor that accepts an object type (by default (default), the object type is an object).
It has a “call” function (by default it is empty), it is called every time the scene changes (every tick). (In one of the “control” cycles, each object is called, the call to the object is called “call”,
those. each object is called, so the base class must contain this method).
The “destruct” method is responsible for removing an object from the scene.

Базовый класс который представляет собой любой объект на сцене,у него есть конструктор,который принимает тип объекта(по дефолту(по умолчанию) тип объекта - это объект).
У есть функция "call"(по умолчанию она пустая),она вызывается каждую смену сцены(каждый тик).(В одном из цикла "control" вызывается каждый объект,вызов объекта это и есть "call",
т.е. каждый объект вызывается ,поэтому базовый класс должен содержать этот метод).
Метод "destruct" отвечает за удаление объекта со сцены.
    """
    def __init__(self, type='object'):
        self.type = type
        
    def __call__(self):
        pass
    
    def destruct(self, control):
        try:
            control.objects.remove(self)#переход в control и удаление объекта
        except:
            raise Exception('wtf err')#если объекта нет и от хочет его удалить,выходит ошибка
            