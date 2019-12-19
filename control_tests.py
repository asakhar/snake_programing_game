# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:53:54 2019

@author: Lizerhigh
"""
import unittest
from control import Control
from gameobject import Object

class Control_Tests(unittest.TestCase):
    
    def test_1start(self):
        global game
        game = Control()
   
    def test_2add_object(self):
        local_game = game
        object1 = Object(type='custom_type')
        local_game += object1
        self.assertIn(object1, game.getobjects())
        
    def test_3getbyattr(self):
        self.assertIsNotNone(game.getbyattr(attr='type', value='custom_type'))
        
    def test_4add_auto_snake(self):
        game.addAutoSnake(scriptpath='template.py', color='red', name='test')
        autosnake = game.getbyattr(type='snake', attr='pn', value='autotest')
        self.assertIn(autosnake, game.getobjects(type='snake'))
        self.assertIsNotNone(autosnake)
    
    def test_5run1time(self):
        game(run_once=True)
    
    def test_6remove_object(self):
        local_game = game
        object1 = game.getbyattr(attr='type', value='custom_type')
        self.assertIsNotNone(object1)
        local_game -= object1
        deleted_object1 = game.getbyattr(attr='type', value='custom_type')
        self.assertIsNone(deleted_object1)
        
    def test_7remove_autosnake(self):
        local_game = game
        autosnake = game.getbyattr(type='snake', attr='pn', value='autotest')
        local_game -= autosnake
        deleted_autosnake = game.getbyattr(type='snake', attr='pn', value='autotest')   
        self.assertIsNone(deleted_autosnake)
    
    def test_8run_one_more_time(self):
        game(run_once=True)
    
    def test_9close(self):
        game.close()
        
if __name__ == '__main__':
    unittest.main()