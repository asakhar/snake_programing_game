# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:08:07 2019

@author: Lizerhigh
"""

import pygame
import os
import PySimpleGUI as sg
import traceback
from barrier import Barrier
from gameobject import *
from eventhandler import EventHandler
from snake import Snake
from random import randint
from food import Food
from levelloader import load, openLevel
from pygame.time import Clock
from guinterface import GUI
from turtle import Turtle
from slowdown import Slowdown
from megafood import MegaFood
from json import load as jsonload, dump as jsondump

class Control:
    '''
        Implements scene object class which defines how game works.
        
        Constructor
                bgcolor : pygame.Color - changes the background color
                size : Tuple[2] - defines the size of the window
            
            Initializes game scene.
    '''
    
    def __init__(self, 
                 bgcolor=pygame.Color('White'), 
                 size=(400, 400),  
                 ):
        '''Constructor'''
        # jsondump(gamerules.args, open('gameconfig', 'w'))
        self.gamerules = KeyWordArguments(**jsonload(open('gameconfig', 'r')))
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0.0, 30.0)
        pygame.init()
        self.window = pygame.display.set_mode(size)
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        self.window.fill(bgcolor)
        pygame.display.set_icon(pygame.image.load('images/favicon.png'))
        pygame.display.set_caption("Snake")
        self.objects = []
        self.clock = Clock()
        self.bgcolor = bgcolor
        self.eventhandler = EventHandler()
        self.run = True
        self.nextfood = -randint(*self.gamerules.foodspawnrange)
        self.nextmegafood = -randint(*self.gamerules.megaspawnrange)
        self.nextslowdown = -randint(*self.gamerules.slowspawnrange)
        self.size = size
        self.pause = False
        self.deaths = {}
        self.events = []
        self.gui = GUI(pos=(-7, size[1]+30))
        
    def __iadd__(self, obj):
        '''
        "+=" operator overloading.
        Use to add objects to scene
        '''
        self.objects.append(obj)
        return self
    
    def __call__(self):
        '''
        Call magic function
        Runs the scene
        '''
        while self.run:
            self.events = pygame.event.get()
            self.eventhandler(self)
            if self.run and not self.pause:
                if self.nextfood>=0:
                    self.nextfood = -randint(*self.gamerules.foodspawnrange)
                    while 1:
                        new_f = Food(pos=[
                                randint(0, self.size[0]//10)*10, 
                                randint(0, self.size[1]//10)*10
                                ])
                        if not (new_f.pos in self.getproperty(attr='pos')):
                            break
                    self += new_f
                if self.nextmegafood>=0:
                    self.nextmegafood = -randint(*self.gamerules.megaspawnrange)
                    while 1:
                        new_f = MegaFood(pos=[
                                randint(0, self.size[0]//10)*10, 
                                randint(0, self.size[1]//10)*10
                                ])
                        if not (new_f.pos in self.getproperty(attr='pos')):
                            break
                    self += new_f
                if self.nextslowdown>=0:
                    self.nextslowdown = -randint(*self.gamerules.slowspawnrange)
                    while 1:
                        new_f = Slowdown(pos=[
                                randint(0, self.size[0]//10)*10, 
                                randint(0, self.size[1]//10)*10
                                ])
                        if not (new_f.pos in self.getproperty(attr='pos')):
                            break
                    self += new_f
                deltatime = self.clock.tick()
                self.nextfood += deltatime
                self.nextmegafood += deltatime
                self.nextslowdown += deltatime
                for obj in self.objects:
                    obj(self)
                self.gui(self)
                for i in self.getproperty(type='snake', attr='pn'):
                    cur = self.getbyattr(type='snake', attr='pn', value=i)
                    self.deaths[i] = cur.deaths
                pygame.display.flip()
              
            else:
                pass
            
    def __getitem__(self, index):
        '''
        Getitem overloading
        
        returns object by index
        '''
        return self.objects[index]
    
    def __isub__(self, obj):
        '''
        "-=" operator overloading.
        Use to delete object from scene
        '''
        obj.destruct(self)
        return self
    
    def getproperty(self, type=None, attr='pos'):
        '''
        type : str|None - type of objects for searching the property
        attr : str - property name
        
        returns generator object that yields objects' properties
        '''
        for i in self.objects:
            if (i.type == type)or(type == None):
                if hasattr(i, attr):
                    yield getattr(i, attr)
    
    def getbyattr(self, type=None, attr=None, value=None):
        '''
        type : str|None - type of an object to be returned
        attr : str - name of the property to compare
        value : Any - property value
        
        returns first object from scene which properties' value is equal to "value" arg
        '''
        for i in self.objects:
            if ((i.type == type)or(type == None)) \
              and hasattr(i, attr) and \
              (getattr(i, attr) == value):
                return i
        return None
    
    def getobjects(self, type=None):
        '''
        
        type : str|None - type of objects to be returned
        
        returns generator object that yields every object of given type
        '''
        for i in self.objects:
            if (i.type == type)or(type == None):
                yield i
                
    def addAutoSnake(self, scriptpath : str, color, name : str = ''):
        '''
        scriptpath : str - path to the snake script file(e.g. snackescript.py)
        name : str - the name of snake to be spawned
        
        Loads custom script and spawns new snake
        
        If file can't be found or another exception is thrown shows an error messasage
        '''
        while 1:
            try:
                f = open(scriptpath, 'r')
                lines = ''.join(f.readlines())+'\nControl.script = Behavior()'
                f.close()
                exec(lines)
                autosnake = Snake.spawn(
                        self, 
                        color, 
                        'auto'+name, 
                        Control.script, 
                        stdir=RIGHT
                        )
                self += autosnake
                return
            except FileNotFoundError as e:
                errorAlert(*traceback.format_exception(type(e), e, 
                                                       e.__traceback__))
                #scriptapath = self.eventhandler.file_dialog(scriptapath)  Depricated
            except Exception as e:
                errorAlert(*traceback.format_exception(type(e), e, 
                                                       e.__traceback__))
                break
        
def errorAlert(*text):
    '''
    Shows an error message in new window
    '''
    layout = [
            [sg.Text(x, key='label', font='Hack 12')] for x in text] \
            + [[sg.Ok(), sg.Cancel()]
            ]
    window = sg.Window('Error', layout=layout, font='Hack 20')
    while True:
        event, values = window.read()
        if event == 'Ok' or event is None or event =='Cancel':
            window.close()
            return event
    