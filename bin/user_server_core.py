#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import conf
import json
from user_info import UserInfo
from log import g_log_inst as logger


class ApiHandler(object):

    @classmethod
    def get_uname_by_list(cls, params):
        myself = sys._getframe().f_code.co_name
        log_kw = ', '.join(map(lambda (k, v): '%s=%s' % (k, v), params.items()))
        logger.get().debug('%s begin, %s' % (myself, log_kw))
        try:
            user_list = params['userlist'] if 'userlist' in params else []
            logger.get().debug('get user_list : %s'%(user_list))
            # if user_list empty, return error
            if not user_list:
                rsp = {'errno': 10003, 'errmsg': 'user_list is empty!'}
                return (200, rsp)
            
            res = UserInfo.get_username_list(user_list) 
            if res:
                rsp = {'errno': 0, 'errmsg': 'success', 'results': res}
            else:
                rsp = {'errno': 10001, 'errmsg': 'failed'}
            return (200, rsp)
        except Exception as e:
            logger.get().warn('%s failed, user_list=%s, errmsg=%s' % (myself, params['userlist'], e))
            rsp = {'errno': 10002, 'errmsg': 'get userlist failed'}
            return (200, rsp)

    @classmethod
    def get_uname_by_id(cls, params):
        myself = sys._getframe().f_code.co_name
        log_kw = ', '.join(map(lambda (k, v): '%s=%s' % (k, v), params.items()))
        logger.get().debug('%s begin, %s' % (myself, log_kw))
        try:
            user_id = params['userid']
            res = UserInfo.get_username(user_id)
            if res:
                rsp = {'errno': 0, 'errmsg': 'success', 'results': res}
            else:
                rsp = {'errno': 10001, 'errmsg': 'failed'}
            return (200, rsp)
        except Exception as e:
            logger.get().warn('%s failed, query=%s, errmsg=%s' % (myself, query, e))
            rsp = {'errno': 10002, 'errmsg': 'get username failed'}
            return (200, rsp)

    




 
