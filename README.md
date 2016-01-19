# TelegramBotAPI (unofficial)
Telegram Bot API

ref: https://core.telegram.org/bots/api

also see: [pyTelegramBot](https://github.com/sourcesimian/pyTelegramBot)

## Installation

    pip install https://github.com/sourcesimian/pyTelegramBotAPI/tarball/v0.2#egg=TelegramBotAPI-0.2

## Usage
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

## Integration

You can easily add TelegramBotAPI as an install dependency of your own project, e.g.:

    from setuptools import setup

    setup(
       name="myApp",
       ...
       install_requires=[..., 'TelegramBotAPI==0.2'],
       dependency_links = ['https://github.com/sourcesimian/pyTelegramBotAPI/tarball/v0.2#egg=TelegramBotAPI-0.2',]
    )

This will allow your package to be installed using:

    pip install https://github.com/jbloggs/myApp/tarball/master#egg=myutil-0.1 --process-dependency-links

See: https://pip.pypa.io/en/latest/reference/pip_install.html#vcs-support
