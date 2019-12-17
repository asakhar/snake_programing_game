# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Valeria Domanova
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
    
    kwargs contains such attributes as:
        direction - current direction
        health - current health
        deaths - number of self deaths
        data - 4 rays that describes what snake see. let ray = data[i], so the format would be:
            ray[0] - direction of ray
            ray[1] - type of object laying on this ray (it can be 'snake', 'self' or 'barrier')
            ray[3] - distance to the object from the head of the snake
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
        '''
        return self.some_method(kwargs.direction, kwargs.data)
