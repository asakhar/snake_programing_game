# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Danila Sirotenko
"""

from PIL import Image

def avg(a):
    return sum(a)//len(a)

def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image

def set_pixel(img, i, j, c):
    img[i, j] = (c, c, c)
    
def get_pixel(img, i, j):
    c = img[i, j]
    if sum(c) > 254*3:
        return 1
    else:
        return 0

def openLevel(name):
    img = Image.open(f'images/{name}.png')
    return img, img.size

def load(img, size):
    pa = img.load()
    total_len = size[0]//10
    print('Loading level', end='')
    for i in range(size[0]):
        for j in range(size[1]):
            yield get_pixel(pa, i, j), i, j
        if not i%total_len:
            print('.', end='')
    print('\nSuccess!')
    img.close()
