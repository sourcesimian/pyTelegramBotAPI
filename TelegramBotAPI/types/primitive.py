import os
from TelegramBotAPI.types.type import Type


class Integer(Type):
    def _from_raw(self, primitive):
        self._d = int(primitive)


class String(Type):
    def _from_raw(self, primitive):
        if primitive is None:
            raise TypeError('None is an invalid String')
        self._d = str(primitive)


class Boolean(Type):
    def _from_raw(self, primitive):
        if not isinstance(primitive, bool):
            raise TypeError('Not a Boolean type')
        self._d = bool(primitive)


class Float(Type):
    def _from_raw(self, primitive):
        if not (isinstance(primitive, int) or isinstance(primitive, float)):
            raise TypeError('Not a Float type')
        self._d = float(primitive)


class InputFile(Type):
    def _from_raw(self, filename):
        if not os.path.isfile(filename):
            raise TypeError('Not a valid file')
        self.__filename = filename

    def _to_raw(self, strict=True):
        return open(self.__filename, 'rb')
