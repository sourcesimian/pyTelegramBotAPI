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
        for k in list(raw.keys()):
            from io import BufferedReader
            if isinstance(raw[k], BufferedReader):
                import os
                files[k] = (os.path.split(raw[k].name)[1], raw[k])
                del raw[k]

        rsp = requests.post(url, data=raw, files=files, proxies=self.__proxies, timeout=self.__timeout)
        if rsp.status_code != 200:
            raise Exception("Server error: %s: %s\n%s\n%s" % (rsp.status_code, url, self.__proxies, rsp.text))
        value = rsp.json()

        if value['ok'] is not True:
            e = Error()
            e._from_raw(value)
            raise Exception("method: %s\nresponse: %s" % (method, e,))

        if isinstance(value['result'], list):
            responses = []
            for result in value['result']:
                m = method._response()
                m._from_raw(result)
                responses.append(m)
            return responses
        else:
            m = method._response()
            m._from_raw(value['result'])
            return m
