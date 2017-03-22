#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/20.

from flask import request, abort
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

from const import *
from utils import check_signature
from . import logger

APP_ID = app.config['WECHAT_APPID']
TOKEN = app.config['WECHAT_TOKEN']
ENCODING_AES_KEY = app.secret_key


@app.route('/wechat', methods=[GET, POST])
@check_signature
def wechat():
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')
    logger.debug('timestamp: {%s}', timestamp)
    logger.debug('nonce: {%s}', nonce)
    logger.debug('encrypt_type: {%s}', encrypt_type)
    logger.debug('msg_signature: {%s}', msg_signature)

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
