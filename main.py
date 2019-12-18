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
from turtleobj import Turtle
from slowdown import Slowdown
from megafood import MegaFood

if __name__=='__main__':
    '''
    Income point
    
    opening level and placing blocks on the scene
    '''
    level, size = openLevel('level1')  #iterate the level and size of the scene
    game = Control(size=(size[0]*10, size[1]*10))
    game += Turtle(pos=[20, 20])
    game += Turtle(pos=[30, 20])
    level_iter = iter(load(level, size))
    while 1: #exception checking
        try:
            el = next(level_iter) # returns the next iterator value
        except:
            el = None # skips element
        if not el:
            break #if not find the element stops
        if not el[0]:
            game += Barrier('block', pos=[el[1]*10, el[2]*10]) #establish barriers and position
    '''keyboard-controlling snake(s)'''
    game += Snake.spawn(game, 'red', 'p2', EventHandler.Behavior(WASD), stdir=STAY)
    game += Snake.spawn(game, 'green', 'p1', EventHandler.Behavior(ARROWS), stdir=STAY)
    '''open template.py in idle'''
#    os.system('start idle -e template.py')
#    os.system('start idle -e snakescript1.py')
    
    '''depricated'''
#    game.addAutoSnake('snakescript.py', 'blue', '0')
#    game.addAutoSnake('snakescript1.py', 'green', '1')
    error1 = False
    '''
    run game and error handling
    '''
    try:  
        game()
    except Exception as e:
        f = open('crashreport.txt', 'w')  # create crashreport and print all exceptions
        f.writelines(traceback.format_exception(type(e), e, e.__traceback__))
        f.close()
        error1 = True
    game.gui.window.close()
    pygame.quit()
    
    if error1 and errorAlert('An error occured while running.', 
                             'See \'crashreport.txt\' for more info.') == 'Ok':
            os.system('crashreport.txt')