# Telegram Bot API (unofficial) in Python 3
An implementation of the [Telegram Bot API](https://core.telegram.org/bots/api) messages
and some simple clients.

Used by:
* [aioTelegramBot](https://github.com/sourcesimian/aioTelegramBot) - An easily customisable bot written in asyncio Python3.
~~* [txTelegramBot](https://github.com/sourcesimian/txTelegramBot) - An easily customisable bot written in Twisted Python3.~~


## Installation

    pip3 install TelegramBotAPI

## Usage
### Requests Client

```
from TelegramBotAPI.client.requestsclient import RequestsClient
from TelegramBotAPI.types.methods import getUpdates, sendMessage

# setup
client = RequestsClient(_token)

# send_message
msg = sendMessage()
msg.chat_id = _user_id
msg.text = 'hello there'

resp = client.send_method(msg)
print(resp)


# poll updates
msg = getUpdates()
msg.timeout = _timeout
msg.limit = _limit
msg.offset = last_id + 1

updates = client.send_method(msg)

for update in updates:
    print(update)
```

### Python asyncio Client
```
import asyncio

from TelegramBotAPI.client.asyncioclient import AsyncioClient
from TelegramBotAPI.types.methods import getUpdates, sendMessage


@asyncio.coroutine
def main():
    client = AsyncioClient(_token)

    # send message
    msg = sendMessage()
    msg.chat_id = _user_id
    msg.text = 'hello there'

    resp = yield from client.send_method(msg)
    print(resp)

    # poll updates
    msg = getUpdates()
    msg.timeout = _timeout
    msg.limit = _limit
    msg.offset = last_id + 1

    updates = yield from client.send_method(msg)

    for update in updates:
        print(update)
```
