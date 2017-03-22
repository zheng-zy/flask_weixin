#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from __init__ import app

GET = 'GET'
POST = 'POST'
TEXT = 'text'
APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']
ENCODING_AES_KEY = app.secret_key

WELCOME_TEXT = u"感谢关注蓝思科技[愉快]\n我是蓝思助手小喵[调皮]\n\n"

COMMAND_TEXT = u"请回复以下关键词开始：\n——————————\n" \
               u"成绩  图书馆  四六级\n\n电话  快递  明信片\n\n签到  音乐  游戏\n\n公交  雷达  天气\n\n校历  新闻  论坛\n\n陪聊  合作\n\n点击左下角切换输入框"
