
class TypeMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        if '__metaclass__' not in attrs:
            Type._Type__type_map[name.lower()] = cls
            from TelegramBotAPI.types.field import Field
            fields = [n for n in dir(cls) if type(getattr(cls, n)) == Field]
            cls._valid_fields = {n.lower(): getattr(cls, n) for n in fields}
            [delattr(cls, n) for n in fields]
        return cls


class Type(object):
    __metaclass__ = TypeMeta

    __type_map = {}
    _fields = None
    _d = None

    def __init__(self, *args):
        for field in self._valid_fields.itervalues():
            field.setup_types()
        if len(args) > 1:
            raise TypeError('%s can take up to 1 argument (%d given)' % (self.__class__.__name__, len(args)))
        if args:
            self._from_raw(args[0])

    def _from_raw(self, raw):
        self._d = {}

        for key in raw:
            if key not in self._valid_fields:
                raise TypeError(key)
            if self._valid_fields[key].list:
                ld = ListDelegate(self._d, key, self._valid_fields[key])
                ld.extend(raw[key])
            else:
                ad = AssignDelegate(self._d, key, self._valid_fields[key])
                ad._from_raw(raw[key])
        for key, field in self._valid_fields.iteritems():
            if field.optional is False and key not in self._d:
                raise TypeError('"%s" is an expected field in %s' % (key, self.__class__.__name__))

        return self._d

    def _to_raw(self, strict=True):
        if self._leaf:
            return self._d
        raw = {}
        for key in self._valid_fields:
            if self._d is not None and key in self._d:
                raw[key] = self._d[key]._to_raw(strict)
            elif strict and self._valid_fields[key].optional is False:
                raise KeyError('"%s" is an expected field in %s' % (key, self.__class__.__name__))
        return raw

    @classmethod
    def _new(cls, value, type=None):
        if type is None:
            type = set(value.keys()).intersection(cls.__type_map.keys())
            assert len(type) == 1
            type = type.pop()
            value = value[type]

        instance = cls.__type_map[type.lower()]()
        instance._from_raw(value)

        return instance

    @classmethod
    def _type(cls, name):
        return cls.__type_map[name.lower()]

    @property
    def _name(self):
        return self.__class__.__name__

    @property
    def _leaf(self):
        return len(self._valid_fields) == 0

    def __setattr__(self, key, value):
        self.__set(key, value)

    def __setitem__(self, key, value):
        self.__set(key, value)

    def __set(self, key, value):
        if key.startswith('_'):
            super(Type, self).__setattr__(key, value)
            return

        name = key.lower()
        if name in self._valid_fields:
            if self._d is None:
                self._d = {}
            ad = AssignDelegate(self._d, name, self._valid_fields[name])
            ad._from_raw(value)
            return
        raise TypeError('"%s" does not have a "%s" field' % (self.__class__.__name__, key))

    def __getattr__(self, key):
        return self.__get(key)

    def __getitem__(self, key):
        return self.__get(key)

    def __get(self, key):
        if not isinstance(key, basestring):
            raise AttributeError("'%s' has no field '%s'" % (self._name, key))
        name = key.lower()
        if self._d and name in self._d:
            if self._d[name]._leaf:
                return self._d[name]._d
            return self._d[name]
        if name in self._valid_fields:
            if self._valid_fields[name].leaf and not self._valid_fields[name].list:
                raise AttributeError("Optional field '%s' not found in '%s'" % (key, self._name))
            if self._d is None:
                self._d = {}
            if self._valid_fields[name].list:
                return ListDelegate(self._d, name, self._valid_fields[name])
            return AssignDelegate(self._d, name, self._valid_fields[name])

        self.__field_error(key)

    def __delattr__(self, key):
        self.__del(key)

    def __delitem__(self, key):
        self.__del(key)

    def __del(self, key):
        name = key.lower()
        del self._d[name]

    def __iter__(self):
        for name in self._d:
            yield name

    def __str__(self):
        return str(self._to_raw(strict=False))

    def __repr__(self):
        return repr(self._to_raw(strict=False))

    def __cmp__(self, other):
        if self._leaf:
            return cmp(self._d, other)
        return cmp(self._to_raw(strict=False), other)

    def __field_error(self, key):
        raise KeyError('"%s" does not have a "%s" field' % (self.__class__.__name__, key))


class Delegate(object):
    def __init__(self, d, key, field):
        self._d = d
        self._key = key
        self._field = field


class AssignDelegate(Delegate):
    def _from_raw(self, raw):
        if type(raw) in self._field.types:
            self._d[self._key] = raw
        else:
            self._d[self._key] = self.__from_raw(raw)

    def __setattr__(self, key, value):
        return self.__set(key, value)

    def __set(self, key, value):
        if key.startswith('_'):
            return super(AssignDelegate, self).__setattr__(key, value)
        if self._key not in self._d:
            self._d[self._key] = None
        self._d[self._key] = self.__from_field(key, value)

    def __getattr__(self, key):
        raise NotImplementedError('Deep nesting not implemented')

    def __from_raw(self, raw):
        last_exception = None
        for type in self._field.types:
            try:
                assert not self._field.list
                value = type()
                value._from_raw(raw)
                return value
            except TypeError, e:
                last_exception = e
        else:
            raise last_exception

    def __from_field(self, key, value):
        last_exception = None
        for type in self._field.types:
            try:
                v = type()
                setattr(v, key, value)
                return v
            except TypeError, e:
                last_exception = e
        else:
            raise last_exception


class ListDelegate(Delegate):
    def __init__(self, d, key, field):
        super(ListDelegate, self).__init__(d, key, field)
        self._l = []
        if self._key not in self._d:
            self._d[self._key] = self

    def append(self, value):
        t = self._field.types[0]()
        t._from_raw(value)
        self._l.append(t)

    def extend(self, values):
        for value in values:
            self.append(value)

    @property
    def _leaf(self):
        return False
        # return self._field.leaf

    def _to_raw(self, strict=True):
        ret = []

        for i in range(len(self._l)):
            v = self._l[i]
            if v:
                ret.append(v._to_raw(strict))
            elif strict:
                raise IndexError('Index [%d] of list "%s" not set' % (i, self._key))
        return ret

    def __setitem__(self, index, value):
        t = self._field.types[0]()
        t._from_raw(value)
        self._l[index] = t

    def __getitem__(self, index):
        try:
            v = self._l[index]
            if v is None:
                v = self._field.types[0]()
                self._l[index] = v
            return v
        except IndexError:
            pass
        from itertools import count
        for i in count(len(self._l)):
            if i == index:
                v = self._field.types[0]()
                self._l.append(v)
                return v
            else:
                self._l.append(None)

    def __iter__(self):
        for value in self._l:
            yield value

    def __len__(self):
        return len(self._l)
