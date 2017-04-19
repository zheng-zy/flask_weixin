#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from wechatpy.utils import check_signature

from __init__ import app


def test_check_signature():
    check_signature('token', '3d22888cf1576db744547e8b52bafe48bb93877e', '1490166247', '196186297')
    pass


if __name__ == "__main__":
    app.logger.info("123")
    test_check_signature()
