#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from flask import request, abort
from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.events import BaseEvent
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy.replies import *

from __init__ import logger
from const import *

msg_type_resp = {}  # 存放对应消息类型处理函数


def wechat_response():
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')
    logger.debug('encrypt_type: {%s}', encrypt_type)
    logger.debug('msg_signature: {%s}', msg_signature)

    logger.info('raw message: {%s}', request.data)
    crypto = WeChatCrypto(TOKEN, ENCODING_AES_KEY, APP_ID)
    msg = None
    try:
        msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        logger.debug('decrypted message: {%s}', msg)
    except (InvalidSignatureException, InvalidAppIdException):
        abort(403)
    msg = parse_message(msg)

    try:
        if isinstance(msg, BaseEvent):
            logger.debug('current msg type is: {%s}, event is: {%s}', msg.type, msg.event)
            get_resp_func = msg_type_resp[msg.type + '_' + msg.event]
        elif isinstance(msg, BaseMessage):
            logger.debug('current msg type is: {%s}', msg.type)
            get_resp_func = msg_type_resp[msg.type]
        else:
            get_resp_func = None
        if get_resp_func is None:
            logger.error('msg type is: {%s}, event is: {%s}', msg.type, msg.event)
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
    reply = create_reply(msg.content, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response


@set_msg_type('event_subscribe')
def subscribe_resp(msg, crypto, nonce, timestamp):
    reply = create_reply(WELCOME_TEXT + COMMAND_TEXT, msg)
    response = crypto.encrypt_message(reply.render(), nonce, timestamp)
    return response
