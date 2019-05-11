# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       wangyi
   date：          4/20/19
-------------------------------------------------
   Change Activity:
                   4/20/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import experiment_three.predict as predict
id = 1


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


# websocket连接控制
class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print("有用户接入!!")

    def on_close(self):
        print("有用户离开!!")

    def on_message(self, message):
        global id
        image = eval(message)

        # 保存图片
        input = (np.array(image, dtype=np.uint8)).reshape(28, 28)
        im = Image.fromarray(input)
        if im.mode != 'RGB':
            im = im.convert('RGB')
        path = './static/result/{0}.png'.format(id)
        im.save(path)

        # matplotlib显示
        img = Image.open(path)
        plt.figure("Image")  # 图像窗口名称
        plt.imshow(img, cmap='gray')
        plt.show()

        # 识别
        pic = predict.pre_pic(path)
        result = str(predict.predict(pic)[0])
        print("the predict number is : {0}".format(result))
        self.write_message(result)


        #发送处理后的图片到前端
        # with open(path,"rb") as f:
        #     # b64encode是编码，b64decode是解码
        #     base64_data = base64.b64encode(f.read())
        #     self.write_message(base64_data)

        print("收到一张图片!!!")
        id += 1


def make_app():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

    return tornado.web.Application([
        (r"/", LoginHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "./favicon.ico"}),
        (r"/ws", EchoWebSocket)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
