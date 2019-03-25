# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wangyi
   date：          3/8/19
-------------------------------------------------
   Change Activity:
                   3/8/19:
-------------------------------------------------
"""

__author__ = 'wangyi'

import os
import tornado.ioloop
import tornado.web
import numpy


class MainHandler(tornado.web.RequestHandler):
    first = 0
    second = 0
    third = 0
    people_list = []

    def get(self):
        self.render("index.html")

    def post(self):
        try:
            MainHandler.first = int(self.get_argument('first', None))
            MainHandler.second = int(self.get_argument('second', None))
            MainHandler.third = int(self.get_argument('third', None))
            join_people = self.get_argument('join_people', None)
            MainHandler.people_list = join_people.split(",")
        except:
            message = "请检查输入"
            self.write(message)
            return
        self.render("index.html")


def check(lists, num):
    return num <= len(lists)


class AjaxHandler(tornado.web.RequestHandler):
    first_prizes = []
    second_prizes = []
    third_prizes = []

    def get(self, param):
        first = MainHandler.first
        second = MainHandler.second
        third = MainHandler.third
        people_list = MainHandler.people_list
        if param == "抽一等奖":
            if check(people_list, first):
                for i in range(first):
                    index = get_random(len(people_list))
                    AjaxHandler.first_prizes.append(people_list.pop(index))
                self.render("result.html", first_prizes=AjaxHandler.first_prizes,
                            second_prizes=AjaxHandler.second_prizes,
                            third_prizes=AjaxHandler.third_prizes)
            else:
                self.write("剩余人数不足")
        elif param == "抽二等奖":
            if check(people_list, second):
                for i in range(second):
                    index = get_random(len(people_list))
                    AjaxHandler.second_prizes.append(people_list.pop(index))
                self.render("result.html", first_prizes=AjaxHandler.first_prizes,
                            second_prizes=AjaxHandler.second_prizes,
                            third_prizes=AjaxHandler.third_prizes)
            else:
                self.write("剩余人数不足")
        elif param == "抽三等奖":
            if check(people_list, third):
                for i in range(third):
                    index = get_random(len(people_list))
                    AjaxHandler.third_prizes.append(people_list.pop(index))
                self.render("result.html", first_prizes=AjaxHandler.first_prizes,
                            second_prizes=AjaxHandler.second_prizes,
                            third_prizes=AjaxHandler.third_prizes)
            else:
                self.write("剩余人数不足")
        elif param == "重置":
            AjaxHandler.third_prizes = []
            AjaxHandler.first_prizes = []
            AjaxHandler.second_prizes = []


def get_random(size):
    return numpy.random.randint(size)


def make_app():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ajax/(.+)", AjaxHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
