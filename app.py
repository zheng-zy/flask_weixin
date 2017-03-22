#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/20.

from flask import render_template

from __init__ import logger
from const import *
from response import wechat_response
from utils import check_signature

APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']
ENCODING_AES_KEY = app.secret_key


# from flask.ext.sqlalchemy import SQLAlchemy
# basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =\
# 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html', name='mike')


@app.route('/wechat', methods=[GET, POST])
@check_signature
def wechat():
    resp = wechat_response()
    logger.info('resp: %s', resp)
    return resp


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
