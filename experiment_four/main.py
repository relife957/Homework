# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       wangyi
   date：          6/1/19
-------------------------------------------------
   Change Activity:
                   6/1/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

from datetime import datetime
import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import base64
from PIL import Image
import matplotlib.pyplot as plt
import experiment_four.train as train

id = 1
mapping = {
    'azalea': '杜鹃花',
    'carnation': '康乃馨',
    'Catharanthus': '长春花',
    'hibiscus': '木槿花',
    'rose': '玫瑰花'
}


# 登录页面控制
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.remote_ip)
        self.render('index.html')


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        global id
        data = self.get_argument('img')
        data = base64.b64decode(data.replace('data:image/jpeg;base64,', ''))
        path = './static/result/{0}.jpg'.format(id)
        with open(path, 'wb') as f:
            f.write(data)
            print("receive a image!")

        # matplotlib显示
        img = Image.open(path)
        plt.figure("Image")  # 图像窗口名称
        plt.imshow(img)
        plt.show()

        # 预测
        result = train.flower_recog(path)
        self.write(mapping[result])

        id += 1


def make_app():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True, )

    return tornado.web.Application([
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "./favicon.ico"}),
        (r"/", MainHandler),
        (r"/upload", UploadHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
