# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 18:53:54 2019

@author: Lizerhigh
"""
import unittest
from control import Control
from gameobject import Object

class Control_Tests(unittest.TestCase):

    def setUp(self):
        self.game = Control()
        self.game += Object(type='custom')
        self.game.addAutoSnake(scriptpath='template.py', color='red', name='testdel')
        
    def test_1start(self):
        self.assertIsNotNone(self.game)
   
    def test_2add_object(self):
        object1 = Object(type='custom_type')
        self.game += object1
        self.assertIn(object1, self.game.getobjects())
        
    def test_3getbyattr(self):
        self.assertIsNotNone(self.game.getbyattr(attr='type', value='custom'))
        
    def test_4add_auto_snake(self):
        self.game.addAutoSnake(scriptpath='template.py', color='red', name='test')
        autosnake = self.game.getbyattr(type='snake', attr='pn', value='autotest')
        #self.assertIn(autosnake, game.getobjects(type='snake'))
        self.assertIsNotNone(autosnake)
    
    def test_5run1time(self):
        self.game(run_once=True)
    
    def test_6remove_object(self):
        object1 = self.game.getbyattr(attr='type', value='custom')
        self.game -= object1
        deleted_object1 = self.game.getbyattr(attr='type', value='custom')
        self.assertIsNone(deleted_object1)
        
    def test_7remove_autosnake(self):
        autosnake = self.game.getbyattr(type='snake', attr='pn', value='autotestdel')
        self.game -= autosnake
        deleted_autosnake = self.game.getbyattr(type='snake', attr='pn', value='autotestdel')   
        self.assertIsNone(deleted_autosnake)
    
    def test_8run_two_times(self):
        self.game(run_once=True)
        self.game(run_once=True)
    
    def test_9close(self):
        self.game.close()

    def tearDown(self):
        self.game.close()
    
if __name__ == '__main__':
    unittest.main()
