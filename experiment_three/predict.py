# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     predict
   Description :
   Author :       wangyi
   date：          5/4/19
-------------------------------------------------
   Change Activity:
                   5/4/19:
-------------------------------------------------
"""
__author__ = 'wangyi'
import numpy as np
from PIL import Image
import tensorflow as tf
import mnist_cnn as mnist_interence
import os
from tensorflow.examples.tutorials.mnist import input_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
BATCH_SIZE = 100
# 学习率
LEARNING_RATE_BASE = 0.8
# 学习指数衰减率
LEARNING_RATE_DECAY = 0.99
# 损失函数正则化系数
REGULARIZATION_TATE = 0.0001
# 滑动平均系数
MOVING_AVERAGE_DECAY = 0.99
# 迭代次数
TRAIN_STEP = 300000
# 模型路径
MODEL_PATH = 'model'
# 模型名称
MODEL_NAME = 'model'
# 定义用于输入图片数据的张量占位符，输入样本的尺寸
x = tf.placeholder(tf.float32, shape=[None,
                                      mnist_interence.IMAGE_SIZE,
                                      mnist_interence.IMAGE_SIZE,
                                      mnist_interence.NUM_CHANNEL], name='x-input')
# 定义用于输入图片标签数据的张量占位符，输入样本的尺寸
y_ = tf.placeholder(tf.float32, shape=[None, mnist_interence.OUTPUT_NODE], name='y-input')
# 定义采用方差的正则化函数
regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_TATE)
# 通过interence函数获得计算结果张量
y = mnist_interence.interence(x, True, regularizer)
global_step = tf.Variable(0, trainable=False)

def predict(pic):


    saver = tf.train.Saver()
    with tf.Session() as sess:
        path = os.getcwd() + "/model"
        if os.path.exists(path):
            model_file = tf.train.latest_checkpoint(path)
            saver.restore(sess, model_file)
            step = sess.run(global_step)
            print("successful restore at {0}!".format(step))
        else:
            return 0
            # tf.global_variables_initializer().run()

        prevalue = tf.argmax(y,1)
        preValue = sess.run(prevalue,feed_dict={x:pic})
        return preValue



def pre_pic(picName):
    img = Image.open(picName)
    reIm = img.resize((28, 28), Image.ANTIALIAS)
    im_arr = np.array(reIm.convert('L'))
    threshold = 50
    for i in range(28):
        for j in range(28):
            im_arr[i][j] = 255 - im_arr[i][j]
            if (im_arr[i][j] < threshold):
                im_arr[i][j] = 0
            else:
                im_arr[i][j] = 255

    nm_arr = im_arr.reshape([1, 28, 28, 1])
    nm_arr = nm_arr.astype(np.float32)
    img_ready = np.multiply(nm_arr, 1.0 / 255.0)

    return img_ready


def main():
    picName = './static/result/2.png'
    pic = pre_pic(picName)
    # print(pic)
    print("the predict number is : {0}".format(predict(pic)[0]))

if __name__ == '__main__':
    main()
