# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:25:49 2019

@author: Danila Sirotenko
"""
"""
You need to upload a level image and build a level on it. The image is divided into pixels, if the color of the pixel is (conditionally) black, a block is placed in this place,
if the color is white, nothing is set.
Нужен чтобы загружать картинку уровня и по ней строить сам уровень.Картинка разбивается на пиксели,если цвет пикселя (условно)черный,ставится блок на это место,
если цвет белый,ничего не ставится.
"""

from PIL import Image

def avg(a):
    """
    A function that takes into account the average value of the array to make it convenient in the future.
    Фукция которая считает среднее по массиву, просто чтобы удобно было в дальнейшем. 
    """
    return sum(a)//len(a)

def create_image(i, j):
    """
Create an image with dimensions i, j.
Создать изобрадение с размерами i,j.
    """
  image = Image.new("RGB", (i, j), "white")
  return image

def set_pixel(img, i, j, c): 
    """
    Sets grayscale from 0 to 255,
    (s, s, s) is RGB (color code)
    Ставит на изображение цвет по шкале серого от 0 до 255, 
    (с,с,с) это RGB(цветовой код)
    """
    img[i, j] = (c, c, c)
    
def get_pixel(img, i, j):
    """
    Get the pixel from the image and check its color, if it is white, then it is 1, if black, then 0.
    This is also an auxiliary function. We transmit the image and pixel coordinates there.
    Получить пиксель из изображения и проверить его цвет, если он белый ,то это 1, если черный ,то 0.
    Это тоже вспомогательная функция.Мы передаем туда изображение и координаты пикселя.
    """
    c = img[i, j]
    if sum(c) > 254*3:
        return 1
    else:
        return 0

def openLevel(name):
    """ 
    Open level image.
    Открыть изображение уровня.
    """
    img = Image.open(f'images/{name}.png')#путь к изображению.
    return img, img.size

def load(img, size):
    """
    Load level image. "load" is a generator that receives every time there is a block or not, and its coordinates.
    Подгрузить изображение уровня."load" это генератор, который возвращает каждый раз есть или нет блока, и его координаты.
    """
    pa = img.load()
    total_len = size[0]//10
    print('Loading level', end='')#сначала просто пишет "Loading level"
    for i in range(size[0]):#если остаток от деления равен 0,пишем точку,10 точек это 100% загрузки уровня  # по х
        for j in range(size[1]):#по y
            yield get_pixel(pa, i, j), i, j# генератор, перебирает все пиксели
        if not i%total_len:
            print('.', end='')
    print('\nSuccess!')#уровень загружен(Успех!)
    img.close()
