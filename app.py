#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/20.
import logging

from flask import Flask, request, abort
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.utils import check_signature

app = Flask(__name__)
app.config['WECHAT_APPID'] = 'wx3b602e650c2c8dda'
app.config['WECHAT_SECRET'] = '12e75aabd90ab2e034941f61f0c8d0aa'
app.config['WECHAT_TOKEN'] = 'token'
app.config['DEBUG'] = True
app.secret_key = '882f224578cf4043d6b440520fe97085'  # AppSecret
# QCgz5h5kaixpc7Kb5gYyx7JXwYFRQlf439Bp9us4zZW EncodingAESKey

APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']
ENCODING_AES_KEY = 'QCgz5h5kaixpc7Kb5gYyx7JXwYFRQlf439Bp9us4zZW'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()
GET = 'GET'
POST = 'POST'
TEXT = 'text'


@app.route('/wechat', methods=[GET, POST])
def wechat():
    echo_str = request.args.get('echo_str', '')
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')
    logger.debug('echo_str: {%s}', echo_str)
    logger.debug('signature: {%s}', signature)
    logger.debug('timestamp: {%s}', timestamp)
    logger.debug('nonce: {%s}', nonce)
    logger.debug('encrypt_type: {%s}', encrypt_type)
    logger.debug('msg_signature: {%s}', msg_signature)
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        logger.error('check_signature error')
        abort(403)
    if request.method == GET:
        return echo_str
    else:
        logger.info('raw message: {%s}', request.data)
        crypto = WeChatCrypto(TOKEN, ENCODING_AES_KEY, APP_ID)
        msg = ''
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
            logger.debug('descypted message: {%s}', msg)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        msg = parse_message(msg)
        if msg.type == TEXT:
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply('sorry, can not handle this for now', msg)
        return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
