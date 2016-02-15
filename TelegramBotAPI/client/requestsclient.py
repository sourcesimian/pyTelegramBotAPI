import logging
import requests

from TelegramBotAPI.client.baseclient import BaseClient

log = logging.getLogger(__name__)


class RequestsClient(BaseClient):
    __timeout = 10

    def __init__(self, token, proxy=None, debug=False):
        super(RequestsClient, self).__init__(token, debug)
        self.__proxies = None
        if proxy:
            self.__proxies = {"https": "https://%s" % proxy}

    def send_method(self, method):
        url = self._get_post_url(method)
        data, files = self.__get_post_data_and_files(method)

        rsp = requests.post(url, data=data, files=files,
                            proxies=self.__proxies, timeout=self.__timeout)
        self._check_response_status(rsp.status_code, url, self.__proxies, lambda: rsp.text)

        value = rsp.json()
        return self._interpret_response(value, method)

    def __get_post_data_and_files(self, method):
        raw = method._to_raw()
        if self._debug:
            log.debug('CMD: %s', raw)

        files = {}
        for k in list(raw.keys()):
            from io import BufferedReader
            if isinstance(raw[k], BufferedReader):
                import os
                files[k] = (os.path.split(raw[k].name)[1], raw[k])
                del raw[k]
        return raw, files
