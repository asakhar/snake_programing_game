# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:29:09 2019

@author: EMoldovsky
"""

from gameobject import *
from dataclasses import dataclass
from random import choice

@dataclass
class Behavior:
    dir_order = [UP, LEFT, DOWN, RIGHT]
    
    nearest_food : list = None
    prev_turn : tuple = None
    
    def run(self, kwargs):
        data = kwargs['data']
        cur = kwargs['direction']
        prev = cur.copy()
        if self.nearest_food:
            if self.nearest_food[2] <= 0:
                self.nearest_food = None
            else:
                self.nearest_food[2] -= 10
        if cur == STAY:
            cur = UP
        for ray in data:
            if (ray[1] == 'food')and((not self.nearest_food)or(ray[2] < self.nearest_food[2])):
                self.nearest_food = ray[0]+[ray[2]]
        if (self.nearest_food)and(not contra(prev, self.nearest_food[:2])):
            cur = self.nearest_food[:2]
        i = 0
        rot = 1 if data[self.dir_order.index(prev)][1] != 'self' else -1
        while 1:
            if (cur == data[i%4][0]):
                if (data[i%4][1]=='barrier') or (data[i%4][1]=='self'):
                    if (data[i%4][2]>10)and(not contra(prev, data[i%4][0])):       
                        break
                    else:
                        cur = data[(i+rot)%4][0]
                elif not contra(prev, data[i%4][0]):
                    break
                else:
                    cur = data[(i+rot)%4][0]
            if abs(i) > 17:
                break
            i += rot
        
        return cur 
