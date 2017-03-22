#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/20.

from flask import Flask, request, session
from flask_wechatpy import Wechat, wechat_required
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
from wechatpy.replies import create_reply
from wechatpy.utils import check_signature

app = Flask(__name__)
app.config['WECHAT_APPID'] = 'wx3b602e650c2c8dda'
app.config['WECHAT_SECRET'] = '12e75aabd90ab2e034941f61f0c8d0aa'
app.config['WECHAT_TOKEN'] = 'token'
app.config['DEBUG'] = True
app.secret_key = '882f224578cf4043d6b440520fe97085'  # AppSecret
# QCgz5h5kaixpc7Kb5gYyx7JXwYFRQlf439Bp9us4zZW EncodingAESKey

wechat = Wechat(app)


@app.route('/')
# @oauth(scope='snsapi_userinfo')
def index():
    echostr = request.args.get('echostr', '')
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    try:
        check_signature(app.config['WECHAT_TOKEN'], signature, timestamp, nonce)
    except InvalidSignatureException:
        return
    return echostr


@app.route('/clear')
def clear():
    if 'wechat_user_id' in session:
        session.pop('wechat_user_id')
    return "ok"


@app.route('/wechat', methods=['GET', 'POST'])
@wechat_required
def wechat_handler():
    msg = request.wechat_msg
    if msg.type == 'text':
        reply = create_reply(msg.content, message=msg)
    else:
        reply = TextReply(content='hello', message=msg)

    return reply


@app.route('/access_token')
def access_token():
    return "access token: {}".format(wechat.access_token)


# https://mp.weixin.qq.com/advanced/advanced?action=interface&t=advanced/interface&token=1269577494&lang=zh_CN
# http://sumonian.ngrok.cc/access_token
# token
# QCgz5h5kaixpc7Kb5gYyx7JXwYFRQlf439Bp9us4zZW
if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
