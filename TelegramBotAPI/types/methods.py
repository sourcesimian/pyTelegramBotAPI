from TelegramBotAPI.types.type import Type
from TelegramBotAPI.types.field import Field
from TelegramBotAPI.types.primitive import Integer, String, Boolean, Float, InputFile
from TelegramBotAPI.types.compound import ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply
from TelegramBotAPI.types.compound import Message, User, UserProfilePhotos, File


class Method(Type):
    _response = None


class sendMessage(Method):
    _response = Message

    chat_id = Field(Integer)
    text = Field(String)
    disable_web_page_preview = Field(Boolean, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardHide, ReplyKeyboardMarkup, ForceReply, optional=True)
    parse_mode = Field(String, optional=True)


class getUpdates(Method):
    offset = Field(Integer, optional=True)
    limit = Field(Integer, optional=True)
    timeout = Field(Integer, optional=True)


class setWebhook(Method):
    url = Field(String)
    certificate = Field(InputFile, optional=True)


class getMe(Method):
    _response = User

    chat_id = Field(Integer, optional=True)
    text = Field(String, optional=True)
    disable_web_page_preview = Field(Boolean)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class forwardMessage(Method):
    _response = Message

    chat_id = Field(Integer, optional=True)
    from_chat_id = Field(Integer, optional=True)
    message_id = Field(Integer, optional=True)


class sendPhoto(Method):
    _response = Message

    chat_id = Field(Integer)
    photo = Field(InputFile, String)
    caption = Field(String, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendAudio(Method):
    _response = Message

    chat_id = Field(Integer, String, optional=True)
    audio = Field(InputFile, String, optional=True)
    duration = Field(Integer, optional=True)
    performer = Field(String, optional=True)
    title = Field(String, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendDocument(Method):
    _response = Message

    chat_id = Field(Integer, optional=True)
    document = Field(InputFile, String, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendSticker(Method):
    _response = Message

    chat_id = Field(Integer, optional=True)
    sticker = Field(InputFile, String, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendVideo(Method):
    _response = Message

    chat_id = Field(Integer, optional=True)
    video = Field(InputFile, String, optional=True)
    duration = Field(Integer, optional=True)
    caption = Field(String, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendVoice(Method):
    _response = Message

    chat_id = Field(Integer, String, optional=True)
    audio = Field(InputFile, String, optional=True)
    duration = Field(Integer, optional=True)
    reply_to_message_id = Field(Integer, optional=True)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply, optional=True)


class sendLocation(Method):
    _response = Message

    chat_id = Field(Integer, optional=True)
    latitude = Field(Float, optional=True)
    longitude = Field(Float, optional=True)
    reply_to_message_id = Field(Integer)
    reply_markup = Field(ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply)


class sendChatAction(Method):
    chat_id = Field(Integer, optional=True)
    action = Field(String, optional=True)


class getUserProfilePhotos(Method):
    _response = UserProfilePhotos

    user_id = Field(Integer, optional=True)
    offset = Field(Integer)
    limit = Field(Integer)


class getFile(Method):
    _response = File

    file_id = Field(String)
