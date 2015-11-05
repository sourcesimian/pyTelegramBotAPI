from TelegramBotAPI.types.type import Type


class Integer(Type):
    def _from_raw(self, primitive):
        self._d = int(primitive)
        return self._d


class String(Type):
    def _from_raw(self, primitive):
        self._d = unicode(primitive)
        return self._d


class Boolean(Type):
    def _from_raw(self, primitive):
        if not isinstance(primitive, bool):
            raise TypeError('Not a Boolean type')
        self._d = bool(primitive)
        return self._d


class Float(Type):
    def _from_raw(self, primitive):
        if not (isinstance(primitive, int) or isinstance(primitive, float)):
            raise TypeError('Not a Boolean type')
        self._d = float(primitive)
        return self._d


class InputFile(Type):
    def _from_raw(self, filename):
        self.__filename = filename

    def _to_raw(self, *_s):
        return open(self.__filename)
