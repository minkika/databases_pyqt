import json
import sys

sys.path.append('../')
from client.common import *
from client.common.decorators import log


@log
def get_message(client):
    """
    Функция получает сообщение, декодирует байты и возвращает словарь сообщения.
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    """
    Функция конвертирует сообщение (словарь) в JSON, кодирует в байты и отправляет в сокет.
    """
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
