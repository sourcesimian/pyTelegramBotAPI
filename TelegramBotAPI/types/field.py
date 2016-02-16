

class Field(object):
    def __init__(self, *args, **kwargs):
        self.list = False
        self.types = []

        self.optional = kwargs.get('optional', False)
        self.ignore = kwargs.get('ignore', False)
        if self.ignore:
            self.optional = True
            return

        for type in args:
            if isinstance(type, list):
                type = type[0]
                self.list = True
                assert len(args) == 1  # Only allow a single type when using a list
            self.types.append(type)

    def __repr__(self):
        return '<Field(%s)>' % (', '.join([t.__name__ for t in self.types]))

    def setup_types(self):
        """
        The Message object has a circular reference on itself, thus we have to allow
        Type referencing by name. Here we lookup any Types referenced by name and
        replace with the real class.
        """
        def load(t):
            from TelegramBotAPI.types.type import Type
            if isinstance(t, str):
                return Type._type(t)
            assert issubclass(t, Type)
            return t
        self.types = [load(t) for t in self.types]

    @property
    def leaf(self):
        for t in self.types:
            if len(t._valid_fields):
                return False
        return True
