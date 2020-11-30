import logging
import socket
import sys

import server.log.config_server_log

sys.path.append('../')
logger = logging.getLogger('server')


def log(func):
    """
    Функция-декоратор для логирования действий сервера
    """
    def log_saver(*args, **kwargs):
        logger.debug(f'> {func.__name__} args: {args} kwargs: {kwargs} module: {func.__module__}')
        ret = func(*args, **kwargs)
        return ret

    return log_saver


def login_required(func):
    """
    Функция-декоратор, проверяющая авторизацию клиента
    """
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from server.common import ACTION, PRESENCE
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
