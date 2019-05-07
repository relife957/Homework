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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
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


def predict(mnist, image_path):
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
    # 定义平均滑动
    variable_average = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    # 对所有可以训练的变量采用平均滑动
    variable_average_ops = variable_average.apply(tf.trainable_variables())
    # 对预测数据y和实际数据y_计算他们概率的交叉值
    cross_entroy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    # 对各对交叉值求平均，其实是计算y和y_两个随机变量概率分布的交叉熵，交叉熵值越小则表明两种概率分布越接近
    cross_entroy_mean = tf.reduce_mean(cross_entroy)
    # 采用交叉熵和正则化参数作为最后的损失函数
    loss = cross_entroy_mean + tf.add_n(tf.get_collection('loss'))
    # 设置学习率递减方式
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step,
                                               mnist.train.num_examples / BATCH_SIZE, LEARNING_RATE_DECAY)
    # 采用梯度下降的方式计算损失函数的最小值
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss, global_step=global_step)
    # 定义学习操作：采用梯度下降求一次模型训练参数，并对求得的模型参数计算滑动平均值
    train_op = tf.group(train_step, variable_average_ops)

    # 读图片并转为黑白的
    img = Image.open(image_path).convert('L')
    flatten_img = np.reshape(img, 784)
    xs =      #np.array([1 - flatten_img])
    saver = tf.train.Saver()
    with tf.Session() as sess:
        path = os.getcwd() + "/model"
        ckpt = tf.train.latest_checkpoint(path)
        saver.restore(sess, ckpt)
        y = sess.run(tf.argmax(y, 1), feed_dict={x: xs})

    # 因为x只传入了一张图片，取y[0]即可
    # np.argmax()取得独热编码最大值的下标，即代表的数字
    print(image_path)
    print('        -> Predict digit', np.argmax(y[0]))


def main():
    mnist = input_data.read_data_sets('./mni_data', one_hot=True)
    #
    predict(mnist, './test.png')


if __name__ == '__main__':
    main()
