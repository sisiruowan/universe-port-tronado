#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-29 15:56:49
# @Author  : AlexTang (1174779123@qq.com)
# @Link    : http://t1174779123.iteye.com
# @Description : 

import requests

def post_request(userlist):
    _host = 'localhost'
    _port = 1111
    url = 'http://%s:%s/in/userinfo/userlist' % (_host, _port)
    content = {'userlist':userlist}

    rsp = requests.post(url, json=content)
    rsp = rsp.json()
    print rsp
    return rsp

if __name__ == '__main__':
    post_request([1,2,4])