"""
Сервер
"""
import argparse
import configparser
import logging
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import server.log.config_server_log
from server.common.decorators import log
from server.common.utils import *
from server.core import MessageProcessor
from server.database.database import ServerStorage
from server.ui.main_window import MainWindow

logger = logging.getLogger('server')


@log
def parse_args(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    return listen_address, listen_port, gui_flag


@log
def config_load():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    if 'CONFIG' in config:
        return config
    else:
        config.add_section('CONFIG')
        config.set('CONFIG', 'Default_port', str(DEFAULT_PORT))
        config.set('CONFIG', 'Listen_Address', '')
        config.set('CONFIG', 'database_path', '')
        config.set('CONFIG', 'database_file', 'server_database.db3')
        return config


@log
def main():
    config = config_load()
    print(config)
    listen_address, listen_port, show_window = parse_args(
        config['CONFIG']['Default_port'], config['CONFIG']['Listen_Address'])

    database = ServerStorage(
        os.path.join(
            config['CONFIG']['database_path'],
            config['CONFIG']['database_file']))

    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    if show_window:
        while True:
            command = input('exit для завершения работы сервера.')
            if command == 'exit':
                server.running = False
                server.join()
                break
    else:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)
        server_app.exec_()
        server.running = False


if __name__ == '__main__':
    main()
