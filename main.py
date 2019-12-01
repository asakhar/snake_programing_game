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

class Control:
    def __init__(self, bgcolor=pygame.Color('White'), size=(400, 400), foodspawnrange=(200, 700)):
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.window.fill(bgcolor)
        pygame.display.set_icon(pygame.image.load('images/favicon.png'))
        pygame.display.set_caption("Snake")
        self.objects = []
        self.clock = Clock()
        self.bgcolor = bgcolor
        self.eventhandler = EventHandler()
        self.run = True
        self.foodspawn = foodspawnrange
        self.nextfood = -randint(*self.foodspawn)
        self.size = size
        self.pause = False
        self.deaths = {}
        self.events = []
        
    def __iadd__(self, obj):
        self.objects.append(obj)
        return self
    
    def __call__(self):
        while self.run:
            self.events = pygame.event.get()
            self.eventhandler(self)
            if self.run and not self.pause:
                if self.nextfood>=0:
                    self.nextfood = -randint(*self.foodspawn)
                    while 1:
                        new_f = Food(pos=[randint(0, self.size[0]//10)*10, randint(0, self.size[1]//10)*10])
                        if not (new_f.pos in self.getproperty(attr='pos')):
                            break
                    self += new_f
                self.nextfood += self.clock.tick()
                for obj in self.objects:
                    obj(self)
                for i in self.getproperty(type='snake', attr='pn'):
                    cur = self.getbyattr(type='snake', attr='pn', value=i)
                    self.deaths[i] = cur.deaths
                pygame.display.flip()
              
            else:
                pass
            
    def __getitem__(self, index):
        return self.objects[index]
    
    def __isub__(self, obj):
        obj.destruct(self)
        return self
    
    def getproperty(self, type=None, attr='pos'):
        for i in self.objects:
            if (i.type == type)or(type == None):
                if hasattr(i, attr):
                    yield getattr(i, attr)
    
    def getbyattr(self, type=None, attr=None, value=None):
        for i in self.objects:
            if ((i.type == type)or(type == None)) and hasattr(i, attr) and (getattr(i, attr) == value):
                return i
        return None
    
    def getobjects(self, type=None):
        for i in self.objects:
            if (i.type == type)or(type == None):
                yield i
                
    def addAutoSnake(self, scriptname : str, color):
        while 1:
            try:
                f = open(scriptname+'.py', 'r')
                lines = ''.join(f.readlines())+'\nControl.script = Behavior()'#+'\nautosnake.script = run'
                f.close()
                exec(lines)
                autosnake = Snake.spawn(self, color, 'auto'+color, Control.script, stdir=RIGHT)
                self += autosnake
                return
            except FileNotFoundError as e:
                errorAlert(*traceback.format_exception(type(e), e, e.__traceback__))
                scriptname = self.eventhandler.file_dialog(scriptname)
            except Exception as e:
                errorAlert(*traceback.format_exception(type(e), e, e.__traceback__))
        
 
def errorAlert(*text):
    layout = [[sg.Text(x, key='label', font='Hack 12')] for x in text] + [[sg.Ok(), sg.Cancel()]]
    window = sg.Window('Error', layout=layout, font='Hack 20')
    while True:
        event, values = window.read()
        if event == 'Ok' or event is None or event =='Cancel':
            window.close()
            return event
    
if __name__=='__main__':
    level, size = openLevel('level1')
    game = Control(size=(size[0]*10, size[1]*10))
    level_iter = iter(load(level, size))
    while 1:
        try:
            el = next(level_iter)
        except:
            el = None
        if not el:
            break
        if not el[0]:
            game += Barrier('block', pos=[el[1]*10, el[2]*10])
#    game += Snake.spawn(game, 'red', 'p1', EventHandler.playercontroller, controllers=WASD)
#    game += Snake.spawn(game, 'green', 'p2', EventHandler.Behavior(ARROWS))
    os.system('start idle -e snakescript.py')
#    os.system('start idle -e snakescript1.py')
    
    game.addAutoSnake('snakescript', 'blue')
    game.addAutoSnake('snakescript1', 'green')
    error1 = False
    try:
        game()
    except Exception as e:
        f = open('crashreport.txt', 'w')
        f.writelines(traceback.format_exception(type(e), e, e.__traceback__))
        f.close()
        error1 = True
        
    pygame.quit()
    
    if error1 and errorAlert('An error occured while running.', 'See \'crashreport.txt\' for more info.') == 'Ok':
            os.system('crashreport.txt')