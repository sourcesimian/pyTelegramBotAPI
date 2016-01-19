from setuptools import setup, find_packages

setup(
    name="TelegramBotAPI",
    version="0.2",
    description="Telegram Bot API",
    packages=find_packages(exclude=['tests',]),
    install_requires=[
        'pyOpenSSL',
        'service_identity',
        'requests',
    ],
)
