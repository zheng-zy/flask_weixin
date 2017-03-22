#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

import os

from flask_uploads import DEFAULTS

from __init__ import app

GET = 'GET'
POST = 'POST'
TEXT = 'text'
# 微信配置
APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']

# 文件上传配置
folder = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data' + os.sep
app.config['UPLOADED_TEXT_DEST'] = folder
app.config['UPLOADED_TEXT_ALLOW'] = DEFAULTS


ENCODING_AES_KEY = app.secret_key

START_DAY = '2017-03-21'

WELCOME_TEXT = u"感谢关注蓝思科技[愉快]\n我是蓝思助手小喵[调皮]\n\n"

COMMAND_TEXT = u"请回复以下关键词开始：\n——————————\n" \
               u"今日单词(1)  单词练习(2)\n\n" \
               u"成绩  图书馆  四六级\n\n电话  快递  明信片\n\n签到  音乐  游戏\n\n" \
               u"公交  雷达  天气\n\n校历  新闻  论坛\n\n陪聊  合作\n\n点击左下角切换输入框\n\n获取帮助请输入: help"

ERROR_FILE = u'this file is not exist.'
