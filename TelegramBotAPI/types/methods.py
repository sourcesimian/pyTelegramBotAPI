from TelegramBotAPI.types.type import Type
from TelegramBotAPI.types.field import Field
from TelegramBotAPI.types.primitive import Integer, String, Boolean, Float, InputFile
from TelegramBotAPI.types.compound import ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply
from TelegramBotAPI.types.compound import Update, Message, User, UserProfilePhotos, File


class Method(Type):
    _response = None


class getUpdates(Method):
    _response = Update

    offset = Field(Integer, optional=True)
    limit = Field(Integer, optional=True)
    timeout = Field(Integer, optional=True)


class setWebhook(Method):
    url = Field(String)
    certificate = Field(InputFile, optional=True)


class getMe(Method):
    _response = User


class sendMessage(Method):
    _response = Message

    chat_id = Field(Integer, String)
    text = Field(String)
    disable_web_page_preview = Field(Boolean, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardHide, ReplyKeyboardMarkup, ForceReply, optional=True)
    parse_mode = Field(String, optional=True)


class forwardMessage(Method):
    _response = Message

    chat_id = Field(Integer, String)
    from_chat_id = Field(Integer, String)
    message_id = Field(Integer)


class sendPhoto(Method):
    _response = Message

    chat_id = Field(Integer, String)
    photo = Field(InputFile, String)
    caption = Field(String, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendAudio(Method):
    _response = Message

    chat_id = Field(Integer, String)
    audio = Field(InputFile, String)
    duration = Field(Integer, optional=True)
    performer = Field(String, optional=True)
    title = Field(String, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendDocument(Method):
    _response = Message

    chat_id = Field(Integer, String)
    document = Field(InputFile, String)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendSticker(Method):
    _response = Message

    chat_id = Field(Integer, String)
    sticker = Field(InputFile, String)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendVideo(Method):
    _response = Message

    chat_id = Field(Integer, String)
    video = Field(InputFile, String)
    duration = Field(Integer, optional=True)
    caption = Field(String, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendVoice(Method):
    _response = Message

    chat_id = Field(Integer, String)
    audio = Field(InputFile, String)
    duration = Field(Integer, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendLocation(Method):
    _response = Message

    chat_id = Field(Integer, String)
    latitude = Field(Float)
    longitude = Field(Float)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendChatAction(Method):
    _response = Boolean

    chat_id = Field(Integer, String)
    action = Field(String)


class getUserProfilePhotos(Method):
    _response = UserProfilePhotos

    user_id = Field(Integer)
    offset = Field(Integer, optional=True)
    limit = Field(Integer, optional=True)


class getFile(Method):
    _response = File

    file_id = Field(String)


class answerInlineQuery(Method):
    _response = Boolean

    inline_query_id = Field(String)
    results = Field(['InlineQueryResultArticle', ''])
    cache_time = Field(Integer, optional=True)
    is_personal = Field(Boolean, optional=True)
    next_offset = Field(String, optional=True)
