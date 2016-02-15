import logging
import os
from io import BufferedReader
import asyncio
import aiohttp
from aiohttp.helpers import FormData

from TelegramBotAPI.client.baseclient import BaseClient

log = logging.getLogger(__name__)


class AsyncioClient(BaseClient):
    __connector = None

    def __init__(self, token, proxy=None, debug=False):
        super(AsyncioClient, self).__init__(token, debug=debug)

        if proxy:
            self.__connector = aiohttp.ProxyConnector(proxy="http://%s" % proxy)

    @asyncio.coroutine
    def send_method(self, method):
        url = self._get_post_url(method)
        data = self.__get_post_data(method)

        rsp = yield from aiohttp.post(url, data=data, connector=self.__connector)
        self._check_response_status(rsp.status, url,
                                    self.__connector.proxy if self.__connector else None,
                                    lambda: rsp.read())

        value = yield from rsp.json()
        return self._interpret_response(value, method)

    def __get_post_data(self, method):
        raw = method._to_raw()
        if self._debug:
            log.debug('CMD: %s', raw)

        use_multipart = False
        for k in list(raw.keys()):
            if isinstance(raw[k], BufferedReader):
                use_multipart = True
                break

        if not use_multipart:
            return raw

        data = FormData()
        for k in list(raw.keys()):
            if isinstance(raw[k], BufferedReader):
                filename = os.path.split(raw[k].name)[1]
                data.add_field(k, raw[k].read(), filename=filename)
            else:
                data.add_field(k, str(raw[k]))
        return data
