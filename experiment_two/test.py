# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wangyi
   date：          3/12/19
-------------------------------------------------
   Change Activity:
                   3/12/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

from datetime import datetime
import time
import copy


def pop(s):
    for i in s :
        if i == 1 :
            s.remove(i)
    return s


if __name__ == '__main__':
    ls = [1,2,1,4,1,6]
    li = copy.deepcopy(ls)
    li = pop(li)
    print(ls)
    print(li)
