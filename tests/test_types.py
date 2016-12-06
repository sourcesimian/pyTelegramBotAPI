import json
from unittest import TestCase
from tempfile import NamedTemporaryFile


from TelegramBotAPI.types.type import Type
from TelegramBotAPI.types.primitive import Float, String, Integer, InputFile
from TelegramBotAPI.types import Message, User, Chat, ReplyKeyboardMarkup, UserProfilePhotos, ReplyKeyboardHide, Location, File
from TelegramBotAPI.types import sendMessage, sendAudio


_message_rsp = """{"ok": true, "result": {"date": 142703037, "text": "Morning?!", "from": {"username": "botbot", "first_name": "Bot bot", "id": 10272353}, "message_id": 16, "chat": {"username": "joe_soap", "first_name": "Joe", "id": 1624712}}}"""

_update_rsp = """\
{"ok":true,"result":[
{"update_id":756878539,
 "message":{"message_id":2,"from":{"id":15263748,"first_name":"Joe","username":"joe_soap"},"chat":{"id":15263748,"first_name":"Joe","username":"joe_soap"},"date":1434495391,"text":"\/start"}},
{"update_id":756898540,
 "message":{"message_id":3,"from":{"id":15263748,"first_name":"Joe","username":"joe_soap"},"chat":{"id":15263748,"first_name":"Joe","username":"joe_soap"},"date":1434495492,"text":"Any one there?"}}
 ]}"""


from TelegramBotAPI.types.field import Field

class FloatA(Type):
    a = Field(Float)

class FloatB(Type):
    b = Field(FloatA)

class FloatC(Type):
    c = Field(FloatB)

class FloatD(Type):
    d = Field(FloatC)

class StringA(Type):
    a = Field(String)

class StringB(Type):
    b = Field(StringA)

class StringC(Type):
    c = Field(StringB)


class Methods(TestCase):

    def test_primitive(self):
        s = String("Hello there")
        self.assertEqual('Hello there', s._to_raw())

    def test_compount(self):
        u = User({'id': 1234, 'first_name': 'Joe'})
        self.assertEquals(u._to_raw(), {'id': 1234, 'first_name': 'Joe'})

    def test_bad_init(self):
        self.assertRaises(TypeError, Integer, 1, 2)

    def test_new(self):
        res = json.loads(_update_rsp)['result'][0]
        m = Type._new(res)
        m._to_raw()

    def test_new_with_extra(self):
        res = json.loads(_update_rsp)['result'][0]
        res['message']['foo'] = 'bar'
        value = Type._new(res)
        self.assertEquals(value._from_raw_dropped(), {'foo': 'bar'})

    def test_from_raw_with_ignored(self):
        raw = {'file_path': 'photo/file_39.jpg', 'height': 90, 'file_size': 1694, 'file_id': 'abcde', 'width': 90}
        from TelegramBotAPI.types.compound import PhotoSize
        value = PhotoSize()
        value._from_raw(raw)
        self.assertEqual(value._from_raw_found(), len(raw))
        self.assertEquals(value._from_raw_dropped(), {})

    def test_new_with_missing(self):
        res = json.loads(_update_rsp)['result'][0]
        del res['message']['chat']['id']
        self.assertRaises(TypeError, Type._new, res)

        del res['message']['chat']
        self.assertRaises(TypeError, Type._new, res)

    def test_type(self):
        cls = Type._type('message')
        self.assertTrue(issubclass(cls, Type))
        self.assertTrue(issubclass(cls, Message))

        m = cls()
        self.assertTrue(isinstance(m, Message))

    def test_name(self):
        m = Float()
        self.assertEqual('Float', m._name)

        m = Message()
        self.assertEqual('Message', m._name)

        m = sendMessage()
        self.assertEqual('sendMessage', m._name)

    def test_update_new(self):
        res = json.loads(_update_rsp)['result'][0]

        m = Type._new(res)
        res = res['message']

        self.assertEqual(m.date, res['date'])
        self.assertEqual(m.From.username, res['from']['username'])

        r = m._to_raw()
        self.assertEquals(res, r)

    def test_update_new_type(self):
        rsp = json.loads(_message_rsp)['result']

        m = Type._new(rsp, 'Message')
        r = m._to_raw()

        self.assertEquals(rsp, r)

    def test_basic_assign(self):
        m = sendMessage()
        m.chat_id = 1234
        m.text = 'hello there'

        self.assertEqual(1234, m.chat_id)
        self.assertEqual('hello there', m.text)

        ex = {'chat_id': 1234, 'text': 'hello there'}
        self.assertEquals(ex, m._to_raw())

        m.chat_id = 5678

        ex = {'chat_id': 5678, 'text': 'hello there'}
        self.assertEquals(ex, m._to_raw())

    def test_assign_boolean(self):
        m = ReplyKeyboardHide()

        def g():
            m.hide_keyboard = 'true'
        self.assertRaises(TypeError, g)

        m.hide_keyboard = True
        self.assertEqual(True, m.hide_keyboard)

    def test_assign_float(self):
        m = Location()

        def g():
            m.longitude = '10.234'
        self.assertRaises(TypeError, g)

        long = 10.234
        m.longitude = long
        self.assertEqual(long, m.longitude)

    def test_nested_assign(self):
        m = Message()
        m.message_id = 1234
        m.From.first_name = 'First'
        m.From['last_name'] = 'Last'
        m.From.id = 10
        m.chat.id = 4321
        m.chat.first_name = 'Foo'
        m['date'] = 121313

        ex = {'message_id': 1234,
              'from': {'first_name': 'First', 'last_name': 'Last', 'id': 10},
              'chat': {'first_name': 'Foo', 'id': 4321},
              'date': 121313
              }
        self.assertEquals(ex, m._to_raw())

        m.chat.first_name = 'Bar'
        ex['chat']['first_name'] = 'Bar'
        self.assertEquals(ex, m._to_raw())

    def test_nested_deref(self):
        t = StringB()
        t.b.a = 'foo'

        self.assertEqual(3, len(t.b.a))
        self.assertEqual(True, t.b.a.startswith('foo'))

        t = StringC()
        t.c.b.a = 'barr'

        self.assertEqual(4, len(t.c.b.a))
        self.assertEqual(True, t.c.b.a.startswith('barr'))

    def test_deep3_nested_assign(self):
        m = FloatC()
        m.c.b.a = 0.1

        ex = {'c': {'b': {'a': 0.1}}}
        self.assertEqual(ex, m._to_raw())

        self.assertEqual(False, m.c.b.a.is_integer())

        m = FloatC()
        def g():
            m.x.b.a = 0.1
        self.assertRaises(KeyError, g)

        def h():
            m.c.x.a = 0.1
        self.assertRaises(KeyError, h)

        def i():
            m.c.b.x = 0.1
        self.assertRaises(TypeError, i)

    def test_deep4_nested_assign(self):
        m = FloatD()
        m.d.c.b.a = 0.1

        ex = {'d': {'c': {'b': {'a': 0.1}}}}
        self.assertEqual(ex, m._to_raw())

    def test_bad_basic_assign(self):
        m = Message()

        def g():
            m.foo = 'bar'
        self.assertRaises(TypeError, g)

    def test_non_list_index(self):
        m = Message()

        def g():
            return m.chat[1]
        self.assertRaises(TypeError, g)

    def test_bad_list_index(self):
        m = UserProfilePhotos()

        def g():
            return m.photos[2][0]
        self.assertRaises(AttributeError, g)

    def test_bad_nested_assign(self):
        m = Message()

        def g():
            m.From.foo = 'bar'
        self.assertRaises(TypeError, g)

    def test_bad_get(self):
        m = Message()

        def g():
            return m.foo
        self.assertRaises(KeyError, g)

        m.chat.id = 10

        def g():
            return m.chat.foo
        self.assertRaises(KeyError, g)

    def test_mandatory(self):
        m = Message()

        m['date'] = 33242
        m.date = 7165371
        m.chat.last_name = "Soap"

        self.assertRaises(KeyError, m._to_raw)

    def test_del(self):
        m = Message()

        m.date = 7165371
        del m.date

        def g():
            return m.date
        self.assertRaises(AttributeError, g)

        m.date = 7165371
        del m['date']

        def g():
            return m.date
        self.assertRaises(AttributeError, g)

    def test_basic_deref(self):
        m = Message()

        m.date = 1234
        self.assertEqual(1234, m.date)

        del m.date

        def g():
            return m.date
        self.assertRaises(AttributeError, g)

    def test_nested_del(self):
        m = Message()

        m.chat.first_name = 'Joe'
        m.chat.last_name = 'Soap'
        self.assertEqual('Joe', m.chat.first_name)
        self.assertEqual('Soap', m.chat.last_name)

        del m.chat.last_name

        def g():
            return m.chat.last_name
        self.assertRaises(AttributeError, g)

    def test_repr(self):
        m = Message()
        m.date = 1234

        self.assertEquals("<%s %s>" % (m.__class__.__name__, repr({'date': 1234})), repr(m))
        self.assertEquals(repr(1234), repr(m.date))

    def test_str(self):
        m = Message()
        m.date = 1234

        self.assertEquals("<%s %s>" % (m.__class__.__name__, str({'date': 1234})), repr(m))
        d = m.date
        self.assertEquals(str(1234), str(d))

    def test_iterate(self):
        m = Message()

        m.chat.first_name = 'Joe'
        m.chat.last_name = 'Soap'
        m.chat.id = 1234
        m.chat.username = 'joe_soap'

        res = {}
        for f in m.chat:
            res[f] = m.chat[f]

        ex = {'first_name': 'Joe', 'last_name': 'Soap', 'username': 'joe_soap', 'id': 1234}
        self.assertEquals(ex, res)

    def test_text_field_types(self):
        m = Message()

        m.reply_to_message.message_id = 5

    def test_variable_type_assign(self):
        m = Message()

        m.chat.title = 'Foo'
        m.chat.id = 1234

        self.assertEqual(type(m.chat), Chat)

    def test_list_assign_primitive(self):
        m = ReplyKeyboardMarkup()

        m.keyboard.append('a')
        m.keyboard.append('b')

        m.keyboard[0] = 'c'

        r = m._to_raw()

        ex = {'keyboard': ['c', 'b']}
        self.assertEquals(ex, r)

    def test_list_iterate(self):
        m = ReplyKeyboardMarkup()

        m.keyboard.append('a')
        m.keyboard.append('b')

        l = []
        for kb in m.keyboard:
            l.append(kb._to_raw())

        ex = ['a', 'b']
        self.assertEqual(ex, l)

    def test_list_assign_compound(self):
        m = UserProfilePhotos()

        m.total_count = 5  # Set wrong length
        m.photos[0].file_id = 'foo.png'
        m.photos[0].width = 320
        m.photos[0].height = 200

        m.photos[1].file_id = 'bar.png'
        m.photos[1].width = 640
        m.photos[1].height = 400

        r = m._to_raw()

        ex = {'photos': [{'file_id': 'foo.png', 'height': 200, 'width': 320},
                         {'file_id': 'bar.png', 'height': 400, 'width': 640}
                         ],
              'total_count': 2}  # Verify that UserProfilePhotos sets total_count
        self.assertEquals(ex, r)

    def test_list_assign_compound_missing(self):
        m = UserProfilePhotos()

        m.total_count = 3
        m.photos[2].file_id = 'foo.png'
        m.photos[2].width = 320
        m.photos[2].height = 200

        m.photos[0].file_id = 'bar.png'
        m.photos[0].width = 640
        m.photos[0].height = 400

        self.assertRaises(IndexError, m._to_raw)

    def test_not_list_assign(self):
        m = Message()

        def g():
            m.chat[0] = 'foo'
        self.assertRaises(TypeError, g)

    def test_assign_type(self):
        m = Message()
        u = User()

        m.chat = u

    def test_nested_assign_type(self):
        m = Message()
        s = String()

        m.chat.first_name = s

    def test_input_file(self):
        t = NamedTemporaryFile()
        t.write(b'contentcontentcontentcontent')
        t.flush()

        f = InputFile(t.name)

        self.assertEqual(b'contentcontentcontentcontent', f._to_raw().read())
        self.assertEqual(t.name, f._to_raw().name)

    def test_input_file_integration(self):
        t = NamedTemporaryFile()
        t.write(b'lalalalalalalalalala')
        t.flush()

        m = sendAudio()
        m.audio = t.name

        from io import BufferedReader
        self.assertTrue(isinstance(m._to_raw(strict=False)['audio'], BufferedReader))

    def test_message_with_photo(self):
        raw = {'from': {'username': 'mybot', 'first_name': 'My bot', 'id': 100000000}, 'photo': [{'width': 90, 'height': 67, 'file_id': 'AgADBAADrqcxG-n9AQZgjPT5D4Qen5rhjjAABFpmaP_GKjtNk28BAAEC', 'file_size': 629}, {'width': 100, 'height': 75, 'file_id': 'AgADBAADrqcxG-n9AQZgjPT5D4Qen5rhjjAABFpmaP_GKjtNk28BAAEC', 'file_size': 1345}], 'caption': 'What is this?', 'chat': {'username': 'jbloggs', 'first_name': 'Joe', 'type': 'private', 'id': 20000000}, 'date': 1446672894, 'message_id': 131}
        m = Message()
        m._from_raw(raw)

    def test_message_with_photo2(self):
        raw = {'date': 1446760513, 'photo': [{'width': 40, 'file_size': 823, 'file_id': 'AgADBAADOqoxG396-QAB_l-8dsikQCIjMtswAASsEEgWRcFfw0EVAQABAg', 'height': 90}, {'width': 143, 'file_size': 9252, 'file_id': 'AgADBAADOqoxG396-QAB_l-8dsikQCIjMtswAASsEEgWRcFfw0EVAQABAg', 'height': 320}, {'width': 164, 'file_size': 11766, 'file_id': 'AgADBAADOqoxG396-QAB_l-8dsikQCIjMoswAAS1BhTBUPT5Tj8VAQABAg', 'height': 366}], 'from': {'username': 'jbloggs', 'first_name': 'Joe', 'id': 20000000}, 'message_id': 137, 'chat': {'username': 'jbloggs', 'first_name': 'Joe', 'type': 'private', 'id': 2000000}}
        m = Message()
        m._from_raw(raw)

        self.assertFalse(hasattr(m, 'text'))

        def g():
            m.text

        self.assertRaises(AttributeError, g)

    def test_file_url(self):
        token = 'f4co5iuq3oidugr4iquf4lulfiu4bilabl'
        path = 'blah/124312414.jpg'
        exp = "https://api.telegram.org/file/bot%s/%s" % (token, path)

        m = File()
        m.file_id = 1234
        m.file_size = 12345678
        m.file_path = 'blah/124312414.jpg'

        self.assertEqual(exp, m.download_url(token))

    def test_eq(self):
        m1 = Message()
        m1.text = "hello"

        m2 = Message()
        m2.text = "hello"

        self.assertEqual(m1, m2)


if __name__ == '__main__':
    import unittest
    unittest.main()
