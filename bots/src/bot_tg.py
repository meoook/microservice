import logging
from telebot import TeleBot, types
from bots.src.objects import SocialBot, SocialName, SocialNames

logger = logging.getLogger(__name__)


class SocialTelegramBot(SocialBot):

    def __init__(self, pk: int, token: str):
        assert isinstance(token, str), 'invalid token type'
        assert token, 'token not set'
        self.__pk: int = pk
        self.__bot = TeleBot(token)
        self.__log = f'Telegram bot(pk:{pk})'
        logger.info(f'{self.__log} created')

    @property
    def pk(self) -> int:
        return self.__pk

    @property
    def social(self) -> SocialName:
        return SocialNames.TG

    def start(self) -> None:
        self.__bot.message_handlers.clear()
        self.__bot.message_handler(self.__handle_msg, commands=[], regexp=None, func=None, content_types=['text'])
        # self.__bot.message_handler(content_types=['photo', 'video', 'sticker'])
        logger.info(f'{self.__log} start')
        self.__bot.polling(non_stop=True)

    def stop(self) -> None:
        logger.info(f'{self.__log} stop')
        self.__bot.stop_bot()

    def beat(self) -> None:
        logger.debug(f'{self.__log} beat')
        self.__bot.get_me()
        # TODO: amq - answer

    def message(self, chat_id: int, msg: str) -> None:
        if not msg:
            logger.warning(f'{self.__log} sending empty message for chat id: {chat_id}')
            return
        logger.info(f'{self.__log} sending message for chat id: {chat_id}')
        self.__bot.send_message(chat_id, msg)

    def __handle_msg(self, message: types.Message, *args) -> None:
        _user: types.User = message.from_user
        _chat: types.Chat = message.chat
        logger.info(f'{self.__log} income message from chat id: {_chat.id}')

        c_public = _chat.type != 'private'
        c_name = _chat.title if _chat.title else _chat.username
        c_id = _chat.id

        if _user.is_bot is False:
            u_id = _user.id
            u_username = _user.username
            u_language = _user.language_code

        logger.debug(f'Message text: {message.text}')
        logger.debug(f'Message content_type: {message.content_type}')
        logger.debug(f'Message timestamp: {message.date}')
        # TODO: amq - message

