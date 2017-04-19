#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

import re
from datetime import datetime

from flask import request, abort
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.events import BaseEvent
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import *

from const import *

BASE_DIR = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
FOLDER_PATH = folder  # 获取当前文件夹内的Test_Data文件

msg_type_resp = {}  # 存放对应消息类型处理函数


def wechat_response():
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')
    app.logger.debug('encrypt_type: {%s}', encrypt_type)
    app.logger.debug('msg_signature: {%s}', msg_signature)

    app.logger.debug('raw message: {%s}', request.data)
    crypto = WeChatCrypto(TOKEN, ENCODING_AES_KEY, APP_ID)
    msg = None
    try:
        msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        app.logger.debug('decrypted message: {%s}', msg)
    except (InvalidSignatureException, InvalidAppIdException):
        abort(403)
    msg = parse_message(msg)

    try:
        if isinstance(msg, BaseEvent):
            app.logger.debug('current msg type is: {%s}, event is: {%s}', msg.type, msg.event)
            get_resp_func = msg_type_resp[msg.type + '_' + msg.event]
        elif isinstance(msg, BaseMessage):
            app.logger.debug('current msg type is: {%s}', msg.type)
            get_resp_func = msg_type_resp[msg.type]
        else:
            get_resp_func = None
        if get_resp_func is None:
            app.logger.error('msg type is: {%s}, event is: {%s}', msg.type, msg.event)
        response = get_resp_func(msg, crypto, nonce, timestamp)
    except KeyError:
        response = 'success'
    return response


def set_msg_type(msg_type):
    """初始化消息类型对应处理函数装饰器"""

    def decorator(func):
        msg_type_resp[msg_type] = func
        return func

    return decorator


@set_msg_type('text')
def text_resp(msg, crypto, nonce, timestamp):
    response = 'success'
    commands = {
        u'取消': cancel_command,
        u'^\?|^？|^help': all_command,
        u'^1|^今日单词': today_word,
        u'^2|^单词练习': word_practise,
        u'^day': day_txt,
        u'^test': day_test,
        u'^天气|^天氣': get_weather_news,

    }
    command_match = False
    for key_word in commands:
        if re.match(key_word, msg.content):
            resp_func = commands[key_word]
            response = resp_func(msg, crypto, nonce, timestamp)
            command_match = True
            break
    if not command_match:
        reply = create_reply(msg.content, msg)
        response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


@set_msg_type('event_subscribe')
def subscribe_resp(msg, crypto, nonce, timestamp):
    reply = create_reply(WELCOME_TEXT + COMMAND_TEXT, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


def cancel_command():
    pass


def all_command(msg, crypto, nonce, timestamp):
    reply = create_reply(WELCOME_TEXT + COMMAND_TEXT, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


def get_weather_news():
    pass


def today_word(msg, crypto, nonce, timestamp):
    end_day = str(datetime.now())[:10]
    a = datetime.strptime(START_DAY, '%Y-%M-%d')
    b = datetime.strptime(end_day, '%Y-%M-%d')
    c = b - a
    file_path = FOLDER_PATH + os.sep + 'day' + str(c.days) + '.txt'
    content = read_file(file_path)
    reply = create_reply(content, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


def word_practise():
    pass


def day_test(msg, crypto, nonce, timestamp):
    file_path = FOLDER_PATH + os.sep + msg.content + '.txt'
    file_path = file_path.replace('test', 'day', 1)
    content = read_file(file_path, True)
    reply = create_reply(content, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


def day_txt(msg, crypto, nonce, timestamp):
    file_path = FOLDER_PATH + os.sep + msg.content + '.txt'
    content = read_file(file_path)
    reply = create_reply(content, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


def read_file(file_path, pattern=False):
    app.logger.debug('file_path: %s', file_path)
    content = ''
    if os.path.exists(file_path):
        with open(file_path, 'r') as txt:
            num = 0
            while 1:
                line = txt.readline()
                if not line:
                    break
                if len(line) < 5:
                    continue
                if not pattern:
                    content += line
                else:
                    if num % 2 == 0:
                        content += line
                num += 1
    else:
        content = ERROR_FILE
    return content


# print 'testadasdas'.replace('test', 'day', 1)
# print read_file(folder + 'day1.txt', True)
