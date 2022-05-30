import logging
from typing import Callable

from telebot import TeleBot, types

from packages.boss_queue.mq_object import MqBotBossParams, MqBotBossMessage
from .bot_object import SocialBot
from utils.enums import SocialNetwork, MqSource, MqAction

logger = logging.getLogger(__name__)


class SocialTelegramBot(SocialBot):

    def __init__(self, pk: int, token: str, publish: Callable[[bytes], None]):
        assert isinstance(token, str), 'invalid token type'
        assert token, 'token not set'
        self.__pk: int = pk
        self.__bot = TeleBot(token)
        self.__log = f'{self.social.value} bot(pk:{pk})'
        self.__publish = publish
        logger.info(f'{self.__log} created')

    @property
    def pk(self) -> int:
        return self.__pk

    @property
    def social(self) -> SocialNetwork:
        return SocialNetwork.TELEGRAM

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
            logger.warning(f'{self.__log} sending empty message for {chat_id=}')
            return
        logger.info(f'{self.__log} sending message for {chat_id=}')
        self.__bot.send_message(chat_id, msg)

    def __handle_msg(self, message: types.Message, *args) -> None:
        _user: types.User = message.from_user
        _chat: types.Chat = message.chat

        if _user.is_bot is True:
            logger.warning(f'{self.__log} income message from bot chat_id: {_chat.id} - ignored')
            return
        else:
            logger.info(f'{self.__log} income message from chat id: {_chat.id}')

        _params = MqBotBossParams({'pk': self.pk,
                                   'chat_id': _chat.id,
                                   'title': _chat.title if _chat.title else _chat.username,
                                   'public': _chat.type != 'private',
                                   'user_id': _user.id,
                                   'username': _user.username,
                                   'language': _user.language_code,
                                   })

        logger.debug(f'Message timestamp: {message.date}, content_type: {message.content_type}')
        logger.debug(f'Message text: {message.text}')
        _msg = MqBotBossMessage(source=MqSource.BOT, action=MqAction.MSG, params=_params, text=message.text)

    def __publish(self, body: bytes) -> None:
        self.__publish(body)
