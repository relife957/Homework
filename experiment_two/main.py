# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main
   Description :
   Author :       wangyi
   date：          3/9/19
-------------------------------------------------
   Change Activity:
                   3/9/19:
-------------------------------------------------
"""
import os

__author__ = 'wangyi'

from datetime import datetime
import tornado.ioloop
import tornado.web
import tornado.websocket
import copy

packet_map = {}  # 每个聊天室和聊天记录
user_map = {}  # 每个聊天群的request
chat_user = {}  # 每个聊天室每个人在线时的聊天记录
pattern = "%m-%d %H:%M:%S"  # 时间格式


# 登录页面控制
class MainHandler(tornado.web.RequestHandler):
    name_list = set()

    def get(self):
        self.render('login.templates')

    def post(self):
        user_name = self.get_argument('user_name', None)
        self.name_list.add(user_name)
        self.set_secure_cookie('name', user_name)
        self.redirect('/chat', permanent=True)


# 聊天室列表页面控制
class ChatListHandler(tornado.web.RequestHandler):
    chat_list = set()

    def get(self):
        self.render('chat_list.templates', chat_list=self.chat_list)

    def post(self):
        chat_name = self.get_argument('chat_name')
        chat_description = self.get_argument('chat_description')
        self.chat_list.add((chat_name, chat_description))
        # packet_map[chat_name] = []
        user_map[chat_name] = set()
        chat_user[chat_name] = {}
        self.get()


# 聊天室内页面
class ChatHandler(tornado.web.RequestHandler):
    def get(self, param):
        self.set_secure_cookie('chat_name', param)
        user_name = self.get_secure_cookie('name', None).decode()
        # statements = copy.deepcopy(packet_map[param])
        if user_name not in chat_user[param]:
            chat_user[param][user_name] = []
        statements = chat_user[param][user_name]
        self.render('chat.templates', statements=statements, username=user_name, chat_name=param)


# websocket连接控制
class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        chat_name = self.get_secure_cookie('chat_name', None).decode()
        user_name = self.get_secure_cookie('name', None).decode()
        user_map[chat_name].add(self)

        print('{} 进入了 {} at {}'.format(user_name, chat_name, time_string(now())))

    def on_close(self):
        chat_name = self.get_secure_cookie('chat_name', None).decode()
        user_name = self.get_secure_cookie('name', None).decode()
        user_map[chat_name].remove(self)
        print('{} 离开了 {} at {}'.format(user_name, chat_name, time_string(now())))

    def on_message(self, message):
        user_name = self.get_secure_cookie('name', None).decode()
        chat_name = self.get_secure_cookie('chat_name', None).decode()
        pool = user_map[chat_name]
        info = (
            user_name,
            time_string(now()),
            message
        )
        EchoWebSocket.update(tuple_dict(info), pool)
        # packet_map[chat_name].append(info)
        chat_user[chat_name][user_name].append(info)

    @classmethod
    def update(cls, msg, pool):
        for chat in pool:
            chat.write_message(msg)


def make_app():
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        cookie_secret='secret')

    return tornado.web.Application([
        (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": "./favicon.ico"}),
        (r"/", MainHandler),
        (r"/chat", ChatListHandler),
        (r"/chat/(.+)", ChatHandler),
        (r"/ws", EchoWebSocket)
    ], **settings)


def tuple_dict(tuple):
    res = {
        'user_name': tuple[0],
        'time': tuple[1],
        'message': tuple[2]
    }
    return res


def filter_chat(statements, timelag):
    """
    过滤掉不是当前用户在线时期的聊天记录
    :return:
    """
    if timelag[0] == '':
        return []
    flag = timelag[1] == ''
    for statement in statements:
        d = string_time(statement[1])
        if flag:
            if not judge(d, string_time(timelag[0])):
                statements.remove(statement)
                continue
            continue

        if not (judge(d, string_time(timelag[0])) and judge(string_time(timelag[1]), d)):
            statements.remove(statement)
    return statements


def string_time(time_str):
    """
    字符串转datetime
    :param time_str: string
    :return:
    """
    return datetime.strptime(time_str, pattern)


def time_string(time):
    """
    datetime转字符串
    :param time: datetime
    :return:
    """
    return time.strftime(pattern)


def now():
    """
    返回现在时间的datetime
    :return:
    """
    return datetime.now()


def judge(d1, d2):
    """
    判断的d1是否在d2之后
    :param d1: datetime
    :param d2: datetime
    :return: boolean
    """
    return (d1 - d2).seconds >= 0


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
