# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:35:45 2019

@author: lookmnv
"""
import pygame
import sys
import PySimpleGUI as sg
from importlib import import_module
from gameobject import *
from snake import Snake, errorAlert
from dataclasses import dataclass

class EventHandler:
    '''A simple event handling class, which manages callbacks to be executed.'''
    def file_dialog(self, *text):
        layout = [[sg.InputText(text[0], key='input', enable_events=True)], 
                   [sg.Ok()]]
        window = sg.Window('Enter the code file name', 
                           layout=layout, font='Hack 20')
        while True:
            event, values = window.read()
            if event == 'Ok' or event is None or event == 'Enter':
                window.close()
                return values['input']
        
    def __init__(self):
        '''Constructor'''
        self.flag_pause=True
        self.flag_restart=False
    
    class Behavior:     
        '''A simple class, which describes the behavior of the snake, that moves by a keyboard.'''
        def __init__(self, controllers):
            self.controllers = controllers
        
        def run(self, kwargs):
            for event in kwargs.control.events:
                if event.type==KEYDOWN:
                    for i in self.controllers:
                        if (event.key==i[1])and \
                          ((not contra(kwargs.direction, i[0]) \
                            or kwargs.health==1)):
                            return i[0]
            return kwargs.direction
        
    def toggle_pause(self, control, set=None):
        '''A function, which pauses the game
        set- set True or False'''
        if set == None:
            control.pause = not control.pause
        else:
            control.pause = set
        pygame.display.set_caption('Deaths-> '+', '.join([f'{k}: {str(v)}' 
            for k, v in control.deaths.items()]) 
                if control.pause else 'Snake')
    
    def __call__(self, control):
        '''A function of event handler.
        This function describes events, which happends with the snake, when we press certain buttons.
        control - scene.'''
        for event in control.events:
            if event.type==QUIT:
                control.run = False
                control.close()
            if event.type==KEYDOWN:
                if True:
                    player1 = control.getbyattr(type='snake', attr='pn', value='p1')
                    player2 = control.getbyattr(type='snake', attr='pn', value='p2')
                    if player1:
                        if event.key==K_RIGHT and (player1.direction!=[-1, 0] or player1.health==1):
                            player1.direction = [1, 0]
                        if event.key==K_LEFT and (player1.direction!=[1, 0] or player1.health==1):
                            player1.direction = [-1, 0]
                        if event.key==K_UP and (player1.direction!=[0, 1] or player1.health==1):
                            player1.direction = [0, -1]
                        if event.key==K_DOWN and (player1.direction!=[0, -1] or player1.health==1):
                            player1.direction = [0, 1]
                    if player2:
                        if event.key==K_d and (player2.direction!=[-1, 0] or player2.health==1):
                            player2.direction = [1, 0]
                        if event.key==K_a and (player2.direction!=[1, 0] or player2.health==1):
                            player2.direction = [-1, 0]
                        if event.key==K_w and (player2.direction!=[0, 1] or player2.health==1):
                            player2.direction = [0, -1]
                        if event.key==K_s and (player2.direction!=[0, -1] or player2.health==1):
                            player2.direction = [0, 1]
                if event.key==K_r:
                    try:
                        autosnake = control.getbyattr(type='snake', attr='pn', 
                                                      value='auto0')
                        try:
                            control -= autosnake
                        except:
                            pass
                        control.addAutoSnake(self.file_dialog('snakescript1.py'), 'red', 
                                             'auto0')
                        self.toggle_pause(control, False)
                    except Exception as e:
                        errorAlert(str(e))
                if event.key==K_n:
                    try:
                        autosnake = control.getbyattr(type='snake', attr='pn',
                                                      value='auto1')
                        try:
                            control -= autosnake
                        except:
                            pass
                        control.addAutoSnake(self.file_dialog('snakescript.py'), 'green',
                                             'auto1')
                        self.toggle_pause(control, False)
                    except Exception as e:
                        errorAlert(str(e))
                if event.key==K_SPACE:
                    self.toggle_pause(control)
                if event.key==K_ESCAPE:
                    control.run = False