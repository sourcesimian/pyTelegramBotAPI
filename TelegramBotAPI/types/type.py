import logging

log = logging.getLogger(__name__)
_type_map = {}


class TypeMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        if '__metaclass__' not in attrs:
            _type_map[name.lower()] = cls
            from TelegramBotAPI.types.field import Field
            cls._valid_fields = {}
            for n in dir(cls):
                a = getattr(cls, n)
                if isinstance(a, Field):
                    cls._valid_fields[n.lower()] = a
                    delattr(cls, n)
        return cls


class Type(object, metaclass=TypeMeta):
    __type_map = _type_map
    __from_raw_dropped = None
    __from_raw_found = None
    _fields = None
    _d = None

    def __init__(self, *args):
        for field in self._valid_fields.values():
            field.setup_types()
        if len(args) > 1:
            raise TypeError('%s can take up to 1 argument (%d given)' % (self.__class__.__name__,
                                                                         len(args)))
        if args:
            self._from_raw(args[0])

    def _from_raw(self, raw):
        self._d = {}
        self.__from_raw_dropped = {}
        self.__from_raw_found = 0

        for key in raw:
            if key not in self._valid_fields:
                self.__from_raw_dropped[key] = raw[key]
                continue

            if self._valid_fields[key].ignore:
                self.__from_raw_found += 1
                continue

            if self._valid_fields[key].list:
                ld = ListDelegate(self._d, key, self._valid_fields[key])
                ld.extend(raw[key])
            else:
                ad = AssignDelegate(self._d, key, self._valid_fields[key])
                ad._from_raw(raw[key])
            self.__from_raw_found += 1

        for key, field in self._valid_fields.items():
            if field.optional is False and key not in self._d:
                raise TypeError('"%s" is an expected field in %s' % (key, self.__class__.__name__))

        if self.__from_raw_found == 0:
            raise TypeError('No fields were found for % in %s' % (self.__class__.__name__, raw))

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

    def _from_raw_dropped(self):
        if self._leaf:
            return None
        dropped = self.__from_raw_dropped
        for key in self._valid_fields:
            if self._d is not None and key in self._d:
                d = self._d[key]._from_raw_dropped()
                if d:
                    dropped[key] = d
        return dropped

    def _from_raw_found(self):
        if self._leaf:
            return 1
        return self.__from_raw_found

    @classmethod
    def _new(cls, value, type_name=None):
        if type_name is None:
            type_name = set(value.keys()).intersection(list(cls.__type_map.keys()))
            assert len(type_name) == 1
            type_name = type_name.pop()
            value = value[type_name]

        instance = cls.__type_map[type_name.lower()]()
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
        if not isinstance(key, str):
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

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, str(self._to_raw(strict=False)))

    def __eq__(self, other):
        if self._leaf:
            return self._d == other
        return repr(self._to_raw(strict=False)) == repr(other._to_raw(strict=False))

    def __field_error(self, key):
        raise KeyError('"%s" does not have a "%s" field' % (self.__class__.__name__, key))


class Delegate(object):
    def __init__(self, d, key, field):
        self._d = d
        self._key = key
        self._field = field


class AssignDelegate(Delegate):
    def _from_raw(self, raw):
        if any([True for t in self._field.types if isinstance(raw, t)]):
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
        assert not self._field.list

        def upcast(cls, raw):
            try:
                value = cls()
                value._from_raw(raw)
                return value._from_raw_found(), value
            except TypeError as e:
                return -1, e

        candidates = [upcast(cls, raw) for cls in self._field.types]

        best = None
        rank = -1
        for r, v in candidates:
            if r > rank:
                best = v
                rank = r

        if best is None:
            raise TypeError('None of %s accepted: %s : %s' % (self._field.types, raw, candidates))

        return best

    def __from_field(self, key, value):
        last_exception = None
        for cls in self._field.types:
            try:
                v = cls()
                setattr(v, key, value)
                return v
            except TypeError as e:
                last_exception = e
        raise last_exception  # pylint: disable=raising-bad-type


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

    def _from_raw_dropped(self):
        ret = []

        for i in range(len(self._l)):
            v = self._l[i]
            if v:
                d = v._from_raw_dropped()
                if d:
                    ret.append(d)
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


__all__ = ['Type']
