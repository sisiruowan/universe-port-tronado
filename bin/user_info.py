#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-19 12:10:11
# @Author  : AlexTang (1174779123@qq.com)
# @Link    : http://t1174779123.iteye.com
# @Description : 

import os
import codecs
from conf import user_cfg, user_info_fpath
from log import g_log_inst as logger

class UserInfo(object):
    # load user_infos from file
    if os.path,exists(user_info_fpath):
        with codecs.open(user_info_fpath, 'r', 'utf-8') as f:
            user_infos = [x.strip().split('\t') for x in f]
            for user_info in user_infos:
                user_cfg[user_info[0]] = user_info[1]
        print 'load %s user_info from %s success!' % (len(user_cfg), user_info_fpath)
    
    @classmethod
    def get_username(cls, user_id):
        user_id = str(user_id)
        if user_id not in user_cfg:
            return u'没有此用户！'
        return user_cfg[user_id]

    @classmethod
    def get_username_list(cls, id_list):
        usernames = [{'id':x, 'user_name':cls.get_username(x)} for x in id_list]
        return usernames


if __name__ == '__main__':
    logger.start('../log/user_info.log', __name__, 'DEBUG')
    print UserInfo.get_username(1)
    print UserInfo.get_username(10)
    print UserInfo.get_username_list([1,2,3])


