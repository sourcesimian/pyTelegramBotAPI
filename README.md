# Telegram Bot API (unofficial) in Python 3
An implementation of the [Telegram Bot API](https://core.telegram.org/bots/api) messages
and some simple clients.

Used by:
* [txTelegramBot](https://github.com/sourcesimian/txTelegramBot) - An easily customisable bot written in Twisted Python3.


## Installation

    pip3 install TelegramBotAPI

## Usage
### Basic Client
```
from TelegramBotAPI.client.basic import BasicClient
from TelegramBotAPI.types.methods import sendMessage, getUpdates
from TelegramBotAPI.types.compound import Message, File

# setup
client = BasicClient(_token)


# send_message
msg = sendMessage()
msg.chat_id = 1234
msg.text = 'hello there'

client.post(msg)


# poll updates
msg = getUpdates()
msg.timeout = _timeout
msg.limit = _limit
msg.offset = last_id + 1

updates, last_id = client.post(msg)

for update in updates:
    if isinstance(update, Message):
        print update.text
    elif isinstance(update, File):
        url = update.download_url(_token)
```

### Twisted Python Client
The following code fragments demonstrate how to make use of the Twisted client.
```
from TelegramBotAPI.client.twistedclient import TwistedClient

    ...
    multi = service.MultiService()
    
    bot = BotService(...)
    bot.setServiceParent(multi)
    
    client = TwistedClient(token, bot.on_update, proxy=proxy)
    client.setServiceParent(multi)
```

```
class BotService(service.Service):
    _client = None

    @defer.inlineCallbacks
    def startService(self):
        self._client = self.parent.getServiceNamed('telegrambot_client')

    def send_message(self, message):
        return self._client.send_message(message)
```
