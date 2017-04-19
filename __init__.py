#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

import logging

from flask import Flask

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

app = Flask(__name__)
app.config['WECHAT_APPID'] = 'wx3b602e650c2c8dda'
app.config['WECHAT_SECRET'] = '12e75aabd90ab2e034941f61f0c8d0aa'
app.config['WECHAT_TOKEN'] = 'token'
app.config['DEBUG'] = True
app.secret_key = '9c66bc144457b9ba8c63f17f4ad93356'  # AppSecret
