#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from wechatpy.client import WeChatClient

app = Flask(__name__)
# app.config['WECHAT_APPID'] = 'wx3b602e650c2c8dda'
# app.config['WECHAT_SECRET'] = '12e75aabd90ab2e034941f61f0c8d0aa'
# app.config['WECHAT_TOKEN'] = 'token'
# app.config['DEBUG'] = True
# app.secret_key = '9c66bc144457b9ba8c63f17f4ad93356'  # AppSecret

app.config['WECHAT_APPID'] = 'wx2dcd9b41a9c7a22e'
app.config['WECHAT_SECRET'] = '1ea92c18d7fe0baf783b44123328b1a9'
app.config['WECHAT_TOKEN'] = 'token'
app.config['DEBUG'] = True
app.secret_key = ''  # AppSecret

client = WeChatClient(app.config['WECHAT_APPID'], app.config['WECHAT_SECRET'])
client.fetch_access_token()

# 记录日志
handler = RotatingFileHandler('./app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)
