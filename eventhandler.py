# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 17:19:06 2019

@author: Lookmnv
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
    
    @dataclass
    class Behavior:     
        ''' A simple class, which describes the behavior of the snake, that moves by a keyboard. '''
        controllers : tuple '''type of the control'''
        
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
        '''A functoin, which pauses the game 
        set - set True or False'''
        if set == None:
            control.pause = not control.pause
        else:
            control.pause = set
        pygame.display.set_caption('Deaths-> '+', '.join([f'{k}: {str(v)}' 
            for k, v in control.deaths.items()]) 
                if control.pause else 'Snake')
    
    def __call__(self, control):
        '''A function of event handler
        conrol - scene'''
        for event in control.events:
            if event.type==QUIT:
                control.run = False
            if event.type==KEYDOWN:
                if False:
                    if event.key==K_RIGHT and (control.direction['p1']!=[-1, 0] or control.getbyattr(type='snake', attr='pn', value='p1').health==1):
                        control.direction['p1'] = [1, 0]
                    if event.key==K_LEFT and (control.direction['p1']!=[1, 0] or control.getbyattr(type='snake', attr='pn', value='p1').health==1):
                        control.direction['p1'] = [-1, 0]
                    if event.key==K_UP and (control.direction['p1']!=[0, 1] or control.getbyattr(type='snake', attr='pn', value='p1').health==1):
                        control.direction['p1'] = [0, -1]
                    if event.key==K_DOWN and (control.direction['p1']!=[0, -1] or control.getbyattr(type='snake', attr='pn', value='p1').health==1):
                        control.direction['p1'] = [0, 1]
                    if event.key==K_d and (control.direction['p2']!=[-1, 0] or control.getbyattr(type='snake', attr='pn', value='p2').health==1):
                        control.direction['p2'] = [1, 0]
                    if event.key==K_a and (control.direction['p2']!=[1, 0] or control.getbyattr(type='snake', attr='pn', value='p2').health==1):
                        control.direction['p2'] = [-1, 0]
                    if event.key==K_w and (control.direction['p2']!=[0, 1] or control.getbyattr(type='snake', attr='pn', value='p2').health==1):
                        control.direction['p2'] = [0, -1]
                    if event.key==K_s and (control.direction['p2']!=[0, -1] or control.getbyattr(type='snake', attr='pn', value='p2').health==1):
                        control.direction['p2'] = [0, 1]
                if event.key==K_r:
                    try:
                        autosnake = control.getbyattr(type='snake', attr='pn', 
                                                      value='autogreen')
                        control -= autosnake
                        control.addAutoSnake(self.file_dialog('snakescript1'), 
                                             'green')
                        self.toggle_pause(control, False)
                    except Exception as e:
                        errorAlert(str(e))
                if event.key==K_n:
                    try:
                        autosnake = control.getbyattr(type='snake', attr='pn', 
                                                      value='autoblue')
                        control -= autosnake
                        control.addAutoSnake(self.file_dialog('snakescript'), 
                                             'blue')
                        self.toggle_pause(control, False)
                    except Exception as e:
                        errorAlert(str(e))
                if event.key==K_SPACE:
                    self.toggle_pause(control)
                if event.key==K_ESCAPE:
                    control.run = False
                