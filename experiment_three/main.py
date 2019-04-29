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
import base64
import tornado.websocket

id = 1


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        global id
        image = self.get_body_argument('imageData')
        path = "./static/result/" + str(id) + ".png"
        image = base64.b64decode(image)
        with open(path, 'wb') as f:
            f.write(image)
        print("收到一张图片!!!")
        id += 1


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index2.html")


# websocket连接控制
class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print("有用户接入!!")

    def on_close(self):
        print("有用户离开!!")

    def on_message(self, message):
        global id
        image = message
        path = "./static/result/" + str(id) + ".png"
        image = base64.b64decode(image)
        with open(path, 'wb') as f:
            f.write(image)
        print("收到一张图片!!!")
        id += 1


def make_app():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

    return tornado.web.Application([
        (r"/submit", MainHandler),
        (r"/", LoginHandler),
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "./favicon.ico"}),
        (r"/ws", EchoWebSocket)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
