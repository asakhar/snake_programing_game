# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Valeria Domanova
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
from control import Control, errorAlert

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
#    game += Snake.spawn(game, 'red', 'p1', EventHandler.Behavior(WASD))
#    game += Snake.spawn(game, 'green', 'p2', EventHandler.Behavior(ARROWS))
#    os.system('start idle -e snakescript.py')
#    os.system('start idle -e snakescript1.py')
    
#    game.addAutoSnake('snakescript.py', 'blue', '0')
#    game.addAutoSnake('snakescript1.py', 'green', '1')
    error1 = False
    try:
        game()
    except Exception as e:
        f = open('crashreport.txt', 'w')
        f.writelines(traceback.format_exception(type(e), e, e.__traceback__))
        f.close()
        error1 = True
    game.gui.window.close()
    pygame.quit()
    
    if error1 and errorAlert('An error occured while running.', 
                             'See \'crashreport.txt\' for more info.') == 'Ok':
            os.system('crashreport.txt')