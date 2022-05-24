import logging
from telebot import TeleBot, types

logger = logging.getLogger(__name__)


class SocialTgBot:
    # TODO: Singleton by token
    def __init__(self, token: str):
        assert isinstance(token, str), 'invalid token type'
        assert token, 'token not set'
        self.__bot = TeleBot(token)

        self.__bot.message_handler(commands=[], regexp=None, func=None, content_types=['text'], chat_types=None)
        self.__bot.message_handler(content_types=['photo', 'video', 'sticker'])

        self.__bot.polling(non_stop=True)

    def __handle_msg(self, message: types.Message) -> None:
        logger.debug(f'Message text: {message.text}')
        logger.debug(f'Message content_type: {message.content_type}')
        logger.debug(f'Message timestamp: {message.date}')
        _user: types.User = message.from_user
        logger.debug(
            f'User id: {_user.id} username: {_user.username} first: {_user.first_name} last: {_user.last_name} full: {_user.full_name} '
            f'lang: {_user.language_code} is_bot: {_user.is_bot}')
        _chat: types.Chat = message.chat
        logger.debug(
            f'Chat id: {_chat.id} username: {_chat.username} last: {_chat.last_name} first: {_chat.first_name} type: {_chat.type} bio: {_chat.bio} '
            f'dsc: {_chat.description} invite_link: {_chat.invite_link} link_id: {_chat.linked_chat_id} '
            f'location: {_chat.location} title: {_chat.title}')

    def send_message(self, chat_id: int, msg: str) -> None:
        if not msg:
            logger.warning(f'Sending empty message for chat id: {chat_id}')
            return
        self.__bot.send_message(chat_id, msg)
