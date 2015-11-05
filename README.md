# TelegramBotAPI (unofficial)
Telegram Bot API

ref: https://core.telegram.org/bots/api


## Installation

    pip install https://github.com/sourcesimian/pyTelegramBotAPI/tarball/master#egg=TelegramBotAPI-0.1

## Integration

You can easily add TelegramBotAPI as an install dependency of your own project, e.g.:

    from setuptools import setup

    setup(
       name="myApp",
       ...
       install_requires=[..., 'TelegramBotAPI==0.1'],
       dependency_links = ['https://github.com/sourcesimian/pyTelegramBotAPI/tarball/master#egg=TelegramBotAPI-0.1',]
    )

This will allow your package to be installed using:

    pip install https://github.com/jbloggs/myApp/tarball/master#egg=myutil-0.1 --process-dependency-links

See: https://pip.pypa.io/en/latest/reference/pip_install.html#vcs-support
