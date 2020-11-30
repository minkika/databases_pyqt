import logging
import socket
import sys

import client.log.config_client_log
import server.log.config_server_log

sys.path.append('../')

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):
    def log_saver(*args, **kwargs):
        logger.debug(f'> {func.__name__} args: {args} kwargs: {kwargs} module: {func.__module__}')
        ret = func(*args, **kwargs)
        return ret

    return log_saver


def login_required(func):
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from client.common import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            is_found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            is_found = True
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        is_found = True
            if not is_found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
