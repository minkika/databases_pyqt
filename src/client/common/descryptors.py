import logging
import sys

if sys.argv[0].find('client') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


class Port:
    def __init__(self):
        pass

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(f'Допустимы адреса с 1024 до 65535. Передан {value}')
            raise TypeError('Некорректрый номер порта')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
