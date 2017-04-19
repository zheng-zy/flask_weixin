#!usr/bin/env python
# coding=utf-8
# Created by zhezhiyong@163.com on 2017/3/22.

from wechatpy.utils import check_signature


def test_check_signature():
    check_signature('token', '45020efaf5bb07833000dab518d0c54bbcc9c5a0', '1492590887', '1221401093')
    pass


if __name__ == "__main__":
    test_check_signature()
