#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/20.

from flask import request, redirect, url_for, render_template
from flask_uploads import UploadSet, configure_uploads
from wechatpy import WeChatClient

from const import *
from response import wechat_response
from utils import check_signature, dir_list

APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']
ENCODING_AES_KEY = app.secret_key

texts = UploadSet('text')

configure_uploads(app, texts)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'text' in request.files:
        file_ = request.files['text']
        file_path = folder + file_.filename
        if os.path.exists(file_path):
            os.remove(file_path)
        filename = texts.save(file_)
        return redirect(url_for('show', name=filename))
    return render_template('upload.html')


@app.route('/data')
def show():
    file_list = dir_list(folder)
    urls = []
    if len(file_list) > 0:
        urls = [str(texts.url(file_)).replace('127.0.0.1:5000', 'abc.guozili.site') for file_ in file_list]
    return render_template('show.html', urls=urls)


@app.route('/')
def index():
    app.logger.info("hello")
    return 'hello'


@app.route('/we_chat', methods=[GET, POST])
@check_signature
def we_chat():
    resp = wechat_response()
    app.logger.info('resp: %s', resp)
    return resp


@app.route('/get_followers', methods=[GET, POST])
def get_followers():
    client = WeChatClient(appid, secret)
    followers = client.user.get_followers()
    app.logger.info(followers)
    return followers

if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
