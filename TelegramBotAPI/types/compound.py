from TelegramBotAPI.types.type import Type
from TelegramBotAPI.types.field import Field
from TelegramBotAPI.types.primitive import Integer, String, Boolean, Float


class Update(Type):
    update_id = Field(Integer)
    message = Field('Message', optional=True)
    inline_query = Field('InlineQuery', optional=True)
    chosen_inline_result = Field('ChosenInlineResult', optional=True)


class User(Type):
    id = Field(Integer)
    first_name = Field(String)
    last_name = Field(String, optional=True)
    username = Field(String, optional=True)


class Chat(Type):
    id = Field(Integer)
    type = Field(String)
    title = Field(String, optional=True)
    username = Field(String, optional=True)
    first_name = Field(String, optional=True)
    last_name = Field(String, optional=True)


class Message(Type):
    message_id = Field(Integer)
    froM = Field(User, optional=True)
    date = Field(Integer)
    chat = Field(User, Chat)
    forward_from = Field(User, optional=True)
    forward_date = Field(Integer, optional=True)
    reply_to_message = Field('Message', optional=True)
    text = Field(String, optional=True)
    audio = Field('Audio', optional=True)
    document = Field('Document', optional=True)
    photo = Field(['PhotoSize'], optional=True)
    sticker = Field('Sticker', optional=True)
    video = Field('Video', optional=True)
    voice = Field('Voice', optional=True)
    caption = Field(String, optional=True)
    contact = Field('Contact', optional=True)
    location = Field('Location', optional=True)
    new_chat_participant = Field(User, optional=True)
    left_chat_participant = Field(User, optional=True)
    new_chat_title = Field(String, optional=True)
    new_chat_photo = Field(['PhotoSize'], optional=True)
    delete_chat_photo = Field(Boolean, optional=True)
    group_chat_created = Field(Boolean, optional=True)


class PhotoSize(Type):
    file_id = Field(String)
    width = Field(Integer)
    height = Field(Integer)
    file_size = Field(Integer, optional=True)
    file_path = Field(ignore=True)


class Audio(Type):
    file_id = Field(String)
    duration = Field(Integer)
    performer = Field(String, optional=True)
    title = Field(String, optional=True)
    mime_type = Field(String, optional=True)
    file_size = Field(Integer, optional=True)


class Document(Type):
    file_id = Field(String)
    thumb = Field(PhotoSize, optional=True)
    file_name = Field(String, optional=True)
    mime_type = Field(String, optional=True)
    file_size = Field(Integer, optional=True)


class Sticker(Type):
    file_id = Field(String)
    width = Field(Integer)
    height = Field(Integer)
    thumb = Field(PhotoSize, optional=True)
    file_size = Field(Integer, optional=True)


class Video(Type):
    file_id = Field(String)
    width = Field(Integer)
    height = Field(Integer)
    duration = Field(Integer)
    thumb = Field(PhotoSize, optional=True)
    mime_type = Field(String, optional=True)
    file_size = Field(Integer, optional=True)


class Voice(Type):
    file_id = Field(String)
    duration = Field(Integer)  # seconds
    mime_type = Field(String, optional=True)
    file_size = Field(Integer, optional=True)


class Contact(Type):
    phone_number = Field(String)
    first_name = Field(String)
    last_name = Field(String, optional=True)
    user_id = Field(Integer, optional=True)


class Location(Type):
    longitude = Field(Float)
    latitude = Field(Float)


class UserProfilePhotos(Type):
    total_count = Field(Integer)
    photos = Field([PhotoSize])

    def _to_raw(self, strict=True):
        setattr(self, 'total_count', len(self._d['photos']))
        return super(UserProfilePhotos, self)._to_raw()


class ReplyKeyboardMarkup(Type):
    keyboard = Field([String])
    resize_keyboard = Field(Boolean, optional=True)
    one_time_keyboard = Field(Boolean, optional=True)
    selective = Field(Boolean, optional=True)


class ReplyKeyboardHide(Type):
    hide_keyboard = Field(Boolean)
    selective = Field(Boolean, optional=True)


class ForceReply(Type):
    force_reply = Field(Boolean)
    selective = Field(Boolean, optional=True)


class File(Type):
    file_id = Field(String)
    file_size = Field(Integer, optional=True)
    file_path = Field(String, optional=True)

    def download_url(self, token):
        return "https://api.telegram.org/file/bot%s/%s" % (token, self.file_path)


class Error(Type):
    error_code = Field(Integer)
    ok = Field(String)
    description = Field(String)


class InlineQuery(Type):
    id = Field(String)
    froM = Field(User)
    query = Field(String)
    offset = Field(String)


class InlineQueryResultArticle(Type):
    type = Field(String)
    id = Field(String)
    title = Field(String)
    message_text = Field(String)
    parse_mode = Field(String)
    disable_web_page_preview = Field(Boolean, optional=True)
    url = Field(String, optional=True)
    hide_url = Field(Boolean, optional=True)
    description = Field(String, optional=True)
    thumb_url = Field(String, optional=True)
    thumb_width = Field(Integer, optional=True)
    thumb_height = Field(Integer, optional=True)


class InlineQueryResultPhoto(Type):
    type = Field(String)
    id = Field(String)
    photo_url = Field(String)
    photo_width = Field(Integer, optional=True)
    photo_height = Field(Integer, optional=True)
    thumb_url = Field(String)
    title = Field(String, optional=True)
    description = Field(String, optional=True)
    caption = Field(String, optional=True)
    message_text = Field(String, optional=True)
    parse_mode = Field(String, optional=True)
    disable_web_page_preview = Field(Boolean, optional=True)


class InlineQueryResultGif(Type):
    type = Field(String)
    id = Field(String)
    gif_url = Field(String)
    gif_width = Field(Integer, optional=True)
    gif_height = Field(Integer, optional=True)
    thumb_url = Field(String)
    title = Field(String, optional=True)
    caption = Field(String, optional=True)
    message_text = Field(String, optional=True)
    parse_mode = Field(String, optional=True)
    disable_web_page_preview = Field(Boolean, optional=True)


class InlineQueryResultMpeg4Gif(Type):
    type = Field(String)
    id = Field(String)
    mpeg4_url = Field(String)
    mpeg4_width = Field(Integer, optional=True)
    mpeg4_height = Field(Integer, optional=True)
    thumb_url = Field(String)
    title = Field(String, optional=True)
    caption = Field(String, optional=True)
    message_text = Field(String, optional=True)
    parse_mode = Field(String, optional=True)
    disable_web_page_preview = Field(Boolean, optional=True)


class InlineQueryResultVideo(Type):
    type = Field(String)
    id = Field(String)
    video_url = Field(String)
    mime_type = Field(String)
    message_text = Field(String)
    parse_mode = Field(String, optional=True)
    disable_web_page_preview = Field(Boolean, optional=True)
    video_width = Field(Integer, optional=True)
    video_height = Field(Integer, optional=True)
    video_duration = Field(Integer, optional=True)
    thumb_url = Field(String)
    title = Field(String)
    description = Field(String, optional=True)


class ChosenInlineResult(Type):
    result_id = Field(String)
    froM = Field(User)
    query = Field(String)
