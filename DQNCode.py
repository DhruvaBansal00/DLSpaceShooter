import sys
import cv2
import tensorflow
import random
import numpy
import MLModifiedSpaceShooter as game
from collections import deque

ACTIONS = 3  # right, left, shoot


def weight_variable(shape):
    initial = tensorflow.truncated_normal(shape, stddev=0.01)
    return tensorflow.Variable(initial)


def bias_variable(shape):
    initial = tensorflow.constant(0.01, shape=shape)
    return tensorflow.Variable(initial)


def conv2d(x, w, stride):
    return tensorflow.nn.conv2d(x, w, strides=[1, stride, stride, 1], padding="SAME")


def max_pool_2x2(x):
    return tensorflow.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


def createNetwork():
    # network weights
    W_conv1 = weight_variable([8, 8, 4, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([4, 4, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([1600, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    s = tensorflow.placeholder("float", [None, 80, 80, 4])

    # hidden layers
    h_conv1 = tensorflow.nn.relu(conv2d(s, W_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tensorflow.nn.relu(conv2d(h_pool1, W_conv2, 2) + b_conv2)
    # h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tensorflow.nn.relu(conv2d(h_conv2, W_conv3, 1) + b_conv3)
    # h_pool3 = max_pool_2x2(h_conv3)

    # h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    h_conv3_flat = tensorflow.reshape(h_conv3, [-1, 1600])

    h_fc1 = tensorflow.nn.relu(tensorflow.matmul(h_conv3_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tensorflow.matmul(h_fc1, W_fc2) + b_fc2

    return s, readout, h_fc1
