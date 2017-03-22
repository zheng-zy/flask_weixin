# !usr/bin/env python  # coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from functools import wraps

from flask import request, abort
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature as cs

from __init__ import logger
from const import *


def check_signature(func):
    """微信签名"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        echo_str = request.args.get('echostr', '')

        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        logger.debug('echo_str: {%s}', echo_str)
        logger.debug('signature: {%s}', signature)
        logger.debug('timestamp: {%s}', timestamp)
        logger.debug('nonce: {%s}', nonce)

        try:
            logger.debug('token: %s', TOKEN)
            cs(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            logger.error('check_signature error')
            abort(403)
        if request.method == GET:
            return echo_str
        return func(*args, **kwargs)

    return decorated_function
