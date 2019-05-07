# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wangyi
   date：          4/21/19
-------------------------------------------------
   Change Activity:
                   4/21/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

from PIL import Image
import matplotlib.pylab as plt
import numpy as np
from prettyprinter import pprint

id = 1


def fill(filename):
    img = Image.open(filename)
    x, y = img.size
    try:
        p = Image.new('RGBA', img.size, (255, 255, 255))
        p.paste(img, (0, 0, x, y), img)
        p.save(filename)
    except:
        pass


def picTo01(filename):
    """
    将图片转化为32*32像素的文件，用0 1表示
    :param filename:
    :return:
    """
    # 打开图片
    img = Image.open(filename).convert('RGBA')

    # 得到图片的像素值
    raw_data = img.load()

    # 将其降噪并转化为黑白两色
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if raw_data[x, y][0] < 90:
                raw_data[x, y] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if raw_data[x, y][1] < 136:
                raw_data[x, y] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if raw_data[x, y][2] > 0:
                raw_data[x, y] = (255, 255, 255, 255)

    # 设置为32*32的大小
    img = img.resize((28, 28), Image.LANCZOS)

    # 进行保存，方便查看
    img.save('test.png')

    # 得到像素数组，为(32,32,4)
    array = plt.array(img)

    # 按照公式将其转为01, 公式： 0.299 * R + 0.587 * G + 0.114 * B

    gray_array = np.zeros((28, 28))

    # 行数
    for x in range(array.shape[0]):
        # 列数
        for y in range(array.shape[1]):
            # 计算灰度，若为255则白色，数值越小越接近黑色
            gary = 0.299 * array[x][y][0] + 0.587 * array[x][y][1] + 0.114 * array[x][y][2]
            # 设置一个阙值，记为0
            if gary == 255:
                gray_array[x][y] = 0
            else:
                # 否则认为是黑色，记为1
                gray_array[x][y] = 1

    # 得到对应名称的txt文件
    global id
    name01 = filename.split('.')[0]
    if name01 == '':
        name01 = "{0}".format(id)
        id += 1
    name01 = name01 + '11.txt'

    # 保存到文件中
    np.savetxt(name01, gray_array, fmt='%d', delimiter='')


def shrink(filename):
    img = Image.open(filename).convert('RGBA')
    img = img.resize((28, 28), Image.LANCZOS)
    img.save('test.png')


from pylab import *


def gray(filename):
    im = array(Image.open(filename).convert('L'), 'f')
    print(im.shape,im.dtype)

#
# def toARGB(filename):
#     img = Image.open(filename)
#     res = array(img)
#     pprint(res)


if __name__ == '__main__':
    filename = './static/result/1.png'
    # toARGB(filename)
    fill(filename)
    # shrink(filename)
    # fill('./test.png')
    picTo01(filename)
    # gray('./test.png')