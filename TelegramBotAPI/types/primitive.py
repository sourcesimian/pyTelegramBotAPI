import os
import io
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
    def _from_raw(self, file):
        if issubclass(file.__class__, io.IOBase):
            if not hasattr(file, 'name'):
                raise ValueError("InputFile as a io.IOBase needs a 'name' attribute: %s" % file)
        elif not os.path.isfile(file):
            raise TypeError('Not a valid file: %s' % file)
        self.__file = file

    def _to_raw(self, strict=True):
        if issubclass(self.__file.__class__, io.IOBase):
            return self.__file
        return open(self.__file, 'rb')

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self.__file))
