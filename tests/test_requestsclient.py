from unittest import TestCase

from TelegramBotAPI.client.requestsclient import RequestsClient
from TelegramBotAPI.types.methods import getUpdates, sendMessage, sendPhoto

import env


class BasicClientTest(TestCase):
    _client = None

    def setUp(self):
        if self._client is None:
            self._client = RequestsClient(env.token, env.proxy)

    def test_poll(self):
        m = getUpdates()
        m.timeout = 5
        m.limit = 5
        updates = self._client.send_method(m)

        for update in updates:
            print(update)

    def test_send(self):
        m = sendMessage()
        m.chat_id = env.uid
        m.text = "Hi there"
        resp = self._client.send_method(m)
        print(resp)

    def test_send_photo(self):
        m = sendPhoto()
        m.chat_id = env.uid
        m.caption = "What is this?"
        import os
        m.photo = os.path.join(os.path.split(__file__)[0], "test.jpg")

        resp = self._client.send_method(m)
        print(resp)

