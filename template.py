# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Valeria Domanova
"""

from gameobject import UP, LEFT, DOWN, RIGHT
from dataclasses import dataclass


@dataclass
class Behavior:
    some_attribute : str
    
    def some_function():
        return UP
    
    def run(self, kwargs):
        return kwargs.direction 
