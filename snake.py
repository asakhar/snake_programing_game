# -*- coding: utf-8 -*-
"""
Created on Fri Dec 2 20:35:09 2019

@author: AnnaZadorozhnikova
"""
import pygame
import PySimpleGUI as sg
import os
import traceback
from pygame.time import Clock
from gameobject import *
from food import Food
from random import randint, choice
from snaketail import SnakeTail
from barrier import Barrier

def errorAlert(*text):
    '''
    Shows an error message in new window
    '''
    layout = [[sg.Text(x, key='label', font='Hack 10')] for x in text] + [[sg.Ok()]]
    window = sg.Window('Error', layout=layout, font='Hack 20')
    while True:
        event, values = window.read()
        if event == 'Ok' or event is None or event =='Cancel':
            window.close()
            return event


class Snake(Object):
    '''
    Implements scene object class which defines snake

    Constructor

                image : image of the object from the folder 'images'
                pn : player number
                script: script of behavior
                pos: position
                size: size of the object

    '''
    def __init__(self, image, pn, script, pos=[30, 10], size=None, stdir=STAY, 
                 deaths=0):
         '''
         Automatic method for construction 
         '''   
        super().__init__(type='snake')
        self.img = pygame.image.load(f'images/{image}.png') if not isinstance(
                image, 
                pygame.Surface
                ) else image
        self.size = size if size else self.img.get_size()
        self.clock = Clock()
        self.clock.tick()
        self.headpos = pos.copy()
        self.normal_speed = 180
        self.speed = 180#80
        self.delayer = 0
        self.health = None
        self.pn = pn
        #self.tail = [SnakeTail(self.img, pos=self.headpos, size=self.size)]
        #self.tail = [[self.headpos[0], self.headpos[1], False]]
        self.tail = []
        self.direction = stdir.copy()
        self.stdir = stdir.copy()
        self.script = script
        self.deaths = deaths
        self.cycles = 0
        self.cycletime = 400
        self.delay = 0
        self.slowdown_timer = None
    
    def respawn(self, control):
        '''
        In case of 'death' deletes current object from the scene and adds the new one by calling function 'spawn'. 
        Death counter updates
        '''
        control -= self
        control += Snake.spawn(control, self.img, self.pn, self.script, 
                               self.stdir, self.deaths+1)
#        drop = [Food(pos=i.pos) for i in self.tail if choice([True]*2+[False]*1)]
        
#        for i in drop:
#            control += i
    
    def get_data(self, control, direction):
        '''
        Function that returns information about the direction of the snake head
        '''
        x = self.headpos[0]
        y = self.headpos[1]
        while 1:
            x += direction[0]*10
            y += direction[1]*10
            obj = control.getbyattr(attr='pos', value=[x, y])
            if obj or (y < 0) or (x < 0) or (x > control.size[0]) or (y > control.size[1]):
                if obj and obj.type == 'snake' and hasattr(obj, 'parentid') and obj.parentid == self.pn:
                    return direction, 'self', abs(self.headpos[1]-y) + abs(self.headpos[0]-x)
                return direction, obj.type if obj else None, abs(self.headpos[1]-y) + abs(self.headpos[0]-x)
    
    def __call__(self, control):
        '''
        Function defines snake actions:
        Gets directions and defines its correctness or rises an Exception
        Reduces health if snake does not get food, then respawns snake
        Respawns snake if it сrashes into the barrier or itself
        Adds health from food and 'megafood'
        Reduces snake speed if it stumbles upon an 'slowdown' element and then raises to normal speed
        '''
        if self.health is None:
            self.health = control.gamerules.start_health
        data = [
                self.get_data(control, UP), 
                self.get_data(control, LEFT), 
                self.get_data(control, DOWN), 
                self.get_data(control, RIGHT)
                ]
        try:
            kwargs = KeyWordArguments(
                    direction=self.direction, 
                    data=data,
                    health=self.health, 
                    control=control,
                    deaths=self.deaths,
                    cycles=self.cycles)
            res = self.script.run(kwargs)
            del kwargs
            if (res not in DIRECTIONS)and(not isinstance(self.script, 
               control.eventhandler.Behavior)):
                raise Exception('Wrong direction!')
        except Exception as e:
            if e.args == ('Wrong direction!', ):
                errorAlert(e, 'Snake script returns invalid direction', 
                           'Direction must be in range: (0, 1), (1, 0), (0, -1), (-1, 0)')
            else:
                errorAlert(*traceback.format_exception(type(e), e, 
                                                       e.__traceback__))
                res = self.direction
            control.eventhandler.toggle_pause(control, True)
            self.respawn(control)
        
        self.direction = res
        
        if self.delay > self.cycletime:
            self.delay = 0
            if control.gamerules.health_reduce:
                self.health -= 1
        
        if self.health <= 0:
            self.respawn(control)
            return
            
        if (self.delayer >= 200 - self.speed)and self.direction!=STAY:
            #self.speed = 50 - self.health*5
            self.cycles += 1
            self.delayer = 0
            self.headpos[0] += self.size[0]*self.direction[0]
            self.headpos[1] += self.size[1]*self.direction[1]
            if (self.headpos in control.getproperty('barrier', attr='pos')):
                self.respawn(control)
                return
            if (self.headpos in control.getproperty('snake', attr='pos')):
                if control.gamerules.encounter_tail == 'set_block_cut':
                    tail = control.getbyattr(type='snake', attr='pos', 
                                             value=self.headpos)
                    snake = control.getbyattr(type='snake', attr='pn', 
                                              value=tail.parentid)
                    if snake.pn == self.pn:
                        self.respawn(control)
                        return
                    try:
                        index = snake.tail.index(tail)
                        snake.health -= index
                        spawn_poss = [x.pos.copy() for x in snake.tail[:index]]
                        for i in range(index):
                                control -= snake.tail.pop(0)
                        for i in spawn_poss:
                            control += Barrier(pos=i.copy(), countdown=10000)
                    except Exception:
                        pass
                elif control.gamerules.encounter_tail == 'set_food':
                    tmp = [x.pos.copy() for x in self.tail]
                    self.respawn(control)
                    for i in tmp:
                        control += Food(pos=i)
                    return
                elif control.gamerules.encounter_tail == 'nothing':
                    self.respawn(control)
                    return
                elif control.gamerules.encounter_tail == 'set_block_self':
                    tmp = [x.pos.copy() for x in self.tail]
                    self.respawn(control)
                    for i in tmp:
                        control += Barrier(pos=i)
                    return
            if self.headpos in control.getproperty(attr='pos', type='food'):
                food = control.getbyattr(type='food', value=self.headpos, 
                                             attr='pos')
                if hasattr(food, 'mega'):
                    self.health += 4
                self.health += 1
                control -= food
                
            if self.headpos in control.getproperty(attr='pos', type='slowdown'):
                self.speed = self.normal_speed//2
                self.slowdown_timer = -4000
            tmp = SnakeTail(self.img, self.pn, pos=self.headpos, size=self.size)
            control += tmp
            self.tail.append(tmp)
            if self.health < len(self.tail):
                control -= self.tail.pop(0)
                
        deltatime = self.clock.tick()
        self.delayer += deltatime
        self.delay += deltatime
        if self.slowdown_timer is not None:
            self.slowdown_timer += deltatime
            if self.slowdown_timer > 0:
                self.slowdown_timer = None
                self.speed = self.normal_speed
        
    def spawn(control, image, pn, script, stdir=STAY, deaths=0):
        '''
        Function that adds Snake to the scene in a random position
        '''
        while 1:
            pos=[randint(2, control.size[0]//10-2)*10, randint(2, 
                 control.size[1]//10-2)*10]
            if not (pos in control.getproperty(attr='pos')):
                break
        return Snake(image, pn, pos=pos, script=script, stdir=stdir, 
                     deaths=deaths)
    
    def destruct(self, control):
        '''
        Function that destructs elements in snake tail
        '''
        for i in self.tail:
            control -= i
            
        super().destruct(control)
        
