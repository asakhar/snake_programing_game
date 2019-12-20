# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 22:06:34 2019

@author: DimasBelousov
"""
import PySimpleGUI as sg
from dataclasses import dataclass
from PySimpleGUI import ThisRow
import os.path
from PIL import Image

def ColorChooserButton_v2(button_text, target=(None, None), image_filename=None, image_data=None, image_size=(None, None),
                       image_subsample=None, tooltip=None, border_width=None, size=(None, None), auto_size_button=None,
                       button_color=None, disabled=False, font=None, bind_return_key=False, focus=False, pad=None,
                       key=None, metadata=None, enable_events=True):
    """Function that returns the button in the window of the pregame interface with all options included, the 
    function itself is inside the main class "GUI"
    """
    return sg.Button(button_text=button_text, button_type=sg.BUTTON_TYPE_COLOR_CHOOSER, target=target,
                  image_filename=image_filename, image_data=image_data, image_size=image_size,
                  image_subsample=image_subsample, border_width=border_width, tooltip=tooltip, size=size,
                  auto_size_button=auto_size_button, button_color=button_color, font=font, disabled=disabled,
                  bind_return_key=bind_return_key, focus=focus, pad=pad, key=key, metadata=metadata, enable_events=enable_events)

def create_from_template(color):
    """ Function that creates an image for the "Snake" from the colour that is chosen by the player. In case the colour is already in 
    template, the function does not create the image but uses the template, otherwise it creates a new one and saves it in the folder "Images".
    The process of making a new coloured image consists of:
    -creation of a new image(RGBA - format with 4x8-bit pixels, size-10x10, colour)
    -creation of file with a directory and transmission of the pixels data(six hexademical numbers, what are inside tuple in var "clr", from the
    ingame menu "Choosing the colour")
    -saving a new image with a new colour 
    """
    new_img = Image.new("RGBA", (10, 10), "white")
    new_pa = new_img.load()
    img = Image.open('images/template.png')
    pa = img.load()
    clr = tuple(map(lambda x: int(x, 16), (color[1:3], color[3:5], color[5:], 
                    'ff')))
    for i in range(10):
        for j in range(10):
            if pa[i, j] == (0,0,0,255):
                new_pa[i, j] = clr
    img.close()
    new_img.save(f'images/{color}.png')

class GUI:
    def __init__(self, pos=(0, 0)):
        """Class is responsible for the pregame window interface, it appears each time the player runs the game.
        Method __init__ launches a constructor inside the class, as it is commonly used in programming,
        -self.layout consists of the main body of the window, sg.Text displays the in-script written text,
        sg.Button displays the button in the window, sg.Filebrowse is responsible for finding scripts in the
        directory of the programme files or outside directory, sg.InputText is responsible for  
        colorchooserbutton is responsible for choosing the
        colour of each snake
        -self.window displays the window with the intop message 
        """
        self.layout = [
                [sg.Text(f'Player{i}', key=f'label{i}'), 
                 sg.FileBrowse('Choose script', key=f'script{i}b', 
                               enable_events=True, target=f'script{i}'),
                 sg.InputText(f'template.py', 
                              key=f'script{i}', visible=False, enable_events=True),
                 sg.InputText(
                f'#{"ff" if not i else "00"}{"ff" if i == 2 else "00"}{"ff" if i == 1 else "00"}', 
                              key=f'color{i}', visible=False, enable_events=True),
                 ColorChooserButton_v2('Player color', key=f'bcolor{i}', 
                                       button_color=('white', 
                f'#{"ff" if not i else "00"}{"ff" if i == 2 else "00"}{"ff" if i == 1 else "00"}'), 
                enable_events=True, target=f'color{i}'),
                 sg.Button('Reload script', key=f'reload{i}'),
                 sg.Button('Disable', key=f'disable{i}')]   
                for i in range(3)
                ]
        self.window = sg.Window('Snake game control panel', 
                                layout=self.layout, location=pos)
    
    def __call__(self, control):
        """Method is called each time the player clicks on the body of pregame window and calls different
        objects as functions
        """
        event, values = self.window(timeout=1)
        if event in ('Exit', 'Quit', None):
            self.window.close()
            control.run = False
            return
        if event.startswith('color'):
            if values[event] == 'None':
                values[event] = '#000000'
                self.window.FindElement(event).update(values[event])
            self.window.FindElement(f'b{event}').update(button_color=('white', 
                                       values[event]))
        elif event.startswith('disable'):
            index = event.replace('disable', '')
            try:
                control -= control.getbyattr(type='snake', attr='pn', 
                                             value=f'auto{index}')
            except:
                pass
        elif event.startswith('reload'):
            index = event.replace('reload', '')
            if not os.path.isfile('images/'+values[f'color{index}']+'.png'):
                create_from_template(values[f'color{index}'])
            try:
                control -= control.getbyattr(type='snake', attr='pn', 
                                             value=f'auto{index}')
            except:
                pass
            control.addAutoSnake(values[f'script{index}'], 
                                 values[f'color{index}'], f'{index}')
            
        return 1
            
        
if __name__=='__main__':        
    a = GUI()
    while a(1):
        pass