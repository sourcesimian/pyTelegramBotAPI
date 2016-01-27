from setuptools import setup, find_packages

setup(
    name="TelegramBotAPI",
    version="0.3",
    description="Telegram Bot API",
    author="Source Simian",
    author_email='sourcesimian@users.noreply.github.com',
    url='https://github.com/sourcesimian/pyTelegramBotAPI',
    download_url="https://github.com/sourcesimian/pyPlugin/tarball/v0.3",
    license='MIT',
    packages=find_packages(exclude=['tests',]),
    install_requires=[
        'pyOpenSSL',
        'service_identity',
        'requests',
    ],
)
