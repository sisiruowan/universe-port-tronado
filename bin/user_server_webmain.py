#!/bin/env python
#-*- encoding: utf-8 -*-


import sys
import signal
import json
from time import time
from tornado import httpserver
from tornado import ioloop
from tornado import web
import user_server_core
from log import g_log_inst as logger


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 0.5


class UserListHandler(web.RequestHandler):
    def post(self):
        start_time = time()
        # parse query params
        params = json.loads(self.request.body)
        # process request
        (status, rsp) = user_server_core.ApiHandler.get_uname_by_list(params)
        if 200 == status:
            self.set_header('content-type', 'application/json')
            self.finish(rsp)
        else:
            self.set_status(404)
            self.finish()
        logger.get().info('%s takes time %0.6f' % (self.__class__.__name__, time() - start_time))

class UserIdHandler(web.RequestHandler):
    def get(self):
        ## parse query params
        start_time = time()
        params = {}
        required_keys = ['userid']
        optional_keys = {'size':1}
        for key in required_keys:
            value = self.get_query_argument(key)
            params[key] = value
        for k, v in optional_keys.items(): 
            value = self.get_query_argument(k, v)
            params[k] = value
        ## process request
        (status, rsp) = user_server_core.ApiHandler.get_uname_by_id(params)
        if 200 == status:
            self.set_header('content-type', 'application/json')
            self.finish(rsp)
        else:
            self.set_status(404)
            self.finish()
        logger.get().info('%s takes time %0.6f' % (self.__class__.__name__, time() - start_time))


def signal_handler(sig, frame):
    logger.get().warn('Caught signal: %s', sig)
    ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
    logger.get().info('begin to stop http server ...')
    server.stop()

    logger.get().info('shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = ioloop.IOLoop.instance()
    deadline = time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logger.get().info('shutdown finished')
    stop_loop()


def main():
    try:
        log_path = './log/user_server.log'
        logger.start(log_path, name = __name__, level = 'DEBUG')
        if 2 != len(sys.argv):
            logger.get().warn('start user_server api failed, argv=%s' % (sys.argv))
            return 1
        port = int(sys.argv[1])

        app_inst = web.Application([
            (r'/in/userinfo/userlist', UserListHandler),
            (r'/in/userinfo/userid', UserIdHandler),
        ], compress_response = True)

        global server
        server = httpserver.HTTPServer(app_inst)
        server.listen(port)

        ## install signal handler, for gracefully shutdown
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        logger.get().info('server start, port=%s' % (port))
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt, e:
        raise


if '__main__' == __name__:
    main()
