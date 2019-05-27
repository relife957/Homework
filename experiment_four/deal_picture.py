# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     deal_picture
   Description :
   Author :       wangyi
   date：          5/26/19
-------------------------------------------------
   Change Activity:
                   5/26/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import random
import cv2


def tailor(pic_path):
    image = cv2.imread(pic_path)
    sp = image.shape

    cropImg = 0
    # height < width
    height = int(sp[0])
    width = int(sp[1])
    if height < width:
        diff = int((width - height) / 2)
        end = width - diff
        cropImg = image[0:height, diff:end]
    elif height > width:
        diff = int((height - width) / 2)
        end = height - diff
        cropImg = image[diff:end, 0:width]

    cropImg = cv2.resize(cropImg, (299, 299))
    cv2.imwrite(pic_path, cropImg)


def deal(pic_path):
    image_raw_data = tf.gfile.FastGFile(pic_path, 'rb').read()
    with tf.Session() as sess:
        img_data = tf.image.decode_jpeg(image_raw_data)
        plt.imshow(img_data.eval())
        plt.show()

        # 上下翻转
        flipped1 = tf.image.flip_up_down(img_data)
        plt.imshow(flipped1.eval())
        plt.show()
        plt.savefig(pic_path[:8] + '1-1.jpg')

        # 左右翻转
        flipped2 = tf.image.flip_left_right(img_data)
        plt.imshow(flipped2.eval())
        plt.show()
        plt.savefig(pic_path[:8] + '1-2.jpg')

        # 对角线翻转
        transposed = tf.image.transpose_image(img_data)
        plt.imshow(transposed.eval())
        plt.show()
        plt.savefig(pic_path[:8] + '1-3.jpg')

        # 在[-max_delta, max_delta]的范围随机调整图片的色相。max_delta的取值在[0, 0.5]之间。
        adjusted = tf.image.random_hue(img_data, 0.5)
        # plt.imshow(adjusted.eval())
        # plt.show()

        # 在[-max_delta, max_delta)的范围随机调整图片的亮度。
        adjusted = tf.image.random_brightness(img_data, max_delta=0.5)
        # plt.imshow(adjusted.eval())
        # plt.show()

        # 在[lower, upper]的范围随机调整图的饱和度。
        adjusted = tf.image.random_saturation(img_data, 0, 5)
        plt.imshow(adjusted.eval())
        plt.show()
        plt.savefig(pic_path[:8] + '1-4.jpg')


def main():
    pic_path = './image/1.jpg'
    tailor(pic_path)
    # deal(pic_path)
    # print(pic_path[:8])


if __name__ == '__main__':
    main()
