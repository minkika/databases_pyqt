"""
Клиент
"""
import argparse
import logging
import os
import sys
from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

import client.log.config_client_log
from client.database.database import DbClients
from client.dialog_start import DialogStart
from client.main_window import ClientMainWindow
from client.transport import ClientTransport
from client.common.decorators import log
from client.common.errors import ServerError
from client.common import *

logger = logging.getLogger('client')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':
    server_address, server_port, client_name, client_passwd = arg_parser()
    client_app = QApplication(sys.argv)

    start_dialog = DialogStart()
    if not client_name or not client_passwd:
        client_app.exec_()

        if start_dialog.is_ok:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            logger.debug(f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, имя пользователя: {client_name}')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    database = DbClients(client_name)

    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        logger.debug("Transport ready.")
        transport.setDaemon(True)
        transport.start()

    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)

    del start_dialog
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()
    transport.transport_shutdown()
    transport.join()