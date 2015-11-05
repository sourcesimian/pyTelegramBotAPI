import requests

from collections import Iterable

from TelegramBotAPI.types.compound import Error
from TelegramBotAPI.types.type import Type


class BasicClient(object):
    __timeout = 10

    def __init__(self, token, proxy=None):
        self.__token = token
        self.__proxies = None
        if proxy:
            self.__proxies = {"https": "https://%s" % proxy}

    def __method_url(self, method):
        return 'https://api.telegram.org/bot%s/%s' % (self.__token, method)

    def post(self, method):
        url = self.__method_url(method._name)
        raw = method._to_raw()
        files = {}
        for k in raw.keys():
            if isinstance(raw[k], file):
                import os
                files[k] = (os.path.split(raw[k].name)[1], raw[k])
                del raw[k]

        rsp = requests.post(url, data=raw, files=files, proxies=self.__proxies, timeout=self.__timeout)
        value = rsp.json()

        if value['ok'] is not True:
            m = Error()
            m._from_raw(value)
            raise m

        if method._response:
            m = method._response()
            m._from_raw(value['result'])
            return m
        elif isinstance(value['result'], Iterable):
            updates = []
            update_id = None
            for result in value['result']:
                updates.append(Type._new(result))
                update_id = max(update_id, result['update_id'])
            return updates, update_id

        raise ValueError("Unhandled message from server: %s" % value)
