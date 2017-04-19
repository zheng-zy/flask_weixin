# !usr/bin/env python  # coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from functools import wraps

from flask import request, abort
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature as cs

from const import *


def check_signature(func):
    """微信签名"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        echo_str = request.args.get('echostr', '')

        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        app.logger.debug('echo_str: {%s}', echo_str)
        app.logger.debug('signature: {%s}', signature)
        app.logger.debug('timestamp: {%s}', timestamp)
        app.logger.debug('nonce: {%s}', nonce)

        try:
            app.logger.debug('token: %s', TOKEN)
            cs(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            app.logger.error('check_signature error')
            abort(403)
        if request.method == GET:
            return echo_str
        return func(*args, **kwargs)

    return decorated_function


def dir_list(root_dir):
    file_list = []
    if root_dir is None:
        raise Exception
    for parent, dir_names, file_names in os.walk(root_dir):  # 三个参数：
        # 分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for file_name in file_names:  # 输出文件信息
            # print "the full name of the file is:" + os.path.join(parent, filename)  # 输出文件路径信息
            file_list.append(file_name)
    return file_list
