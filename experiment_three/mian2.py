# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     mian2
   Description :
   Author :       wangyi
   date：          5/6/19
-------------------------------------------------
   Change Activity:
                   5/6/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

import numpy as np
from flask import Flask, jsonify, render_template, request
import matplotlib.pyplot as plt
from PIL import Image

# webapp
app = Flask(__name__)

i = 1


@app.route('/api/mnist', methods=['POST'])
def mnist():
    global i
    input = (np.array(request.json, dtype=np.uint8)).reshape(28, 28)
    # print(input)
    im = Image.fromarray(input)
    im = im.convert('L')
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im.save('./static/result/{0}.png'.format(i))

    i += 1
    print(111)
    return jsonify(results=[111, 222])


@app.route('/')
def main():
    return render_template('index3.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
