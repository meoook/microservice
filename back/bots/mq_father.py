import logging
from typing import Callable
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from utils.enums import SocialNetwork, MqAction, MqExchange, MqBotRoute
from utils.mq.consumer import MqConsumer
from .mq_object import MqFatherMessage
from .socials.bot_object import SocialBot
from .socials.bot_tg import SocialTelegramBot

logger = logging.getLogger('bot.father')


class BotFatherConsumer(MqConsumer):
    """ AMQ Consumer to control bots """

    __SOCIALS: dict[SocialNetwork, Callable[[int, str, Callable[[bytes], None]], SocialBot]] = {
        SocialNetwork.TELEGRAM: SocialTelegramBot,
        SocialNetwork.INSTAGRAM: SocialTelegramBot,
        SocialNetwork.VKONTAKTE: SocialTelegramBot,
        SocialNetwork.FACEBOOK: SocialTelegramBot,
        SocialNetwork.DISCORD: SocialTelegramBot,
    }

    def __init__(self, mq_url: str):
        super().__init__(mq_url, MqExchange.BOT, 'bot_father', MqBotRoute.FATHER)

        self.__BOTS: dict[int, SocialBot] = {}
        self.__actions: dict[MqAction, Callable[[MqFatherMessage], None]] = {
            MqAction.CREATE: self.__bot_create,
            MqAction.DELETE: self.__bot_delete,
            MqAction.BEAT: self.__bot_heartbeat,
            MqAction.MSG: self.__bot_msg,
        }

        try:
            logger.info(f'Start consuming queue "{self.QUEUE}"')
            self._start(self.__callback)
        except Exception as _err:
            logger.warning(f'Stop consuming queue "{self.QUEUE}" - {_err}')

    def __publish(self, body: bytes) -> None:
        """ Function for bots to put message in queue """
        logger.info('Send mq message')
        self._publish(MqBotRoute.BOSS, body=body)

    def __callback(self, ch: BlockingChannel, method: Basic.Deliver, _: BasicProperties, body: bytes):
        try:
            _msg: MqFatherMessage = MqFatherMessage.from_bytes(body)
        except Exception as _err:
            logger.error(f'Failed to create message from "{body}" - {_err}')
        else:
            self.__do_action(_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __do_action(self, msg: MqFatherMessage) -> None:
        try:
            self.__actions[msg.action](msg)
        except Exception as _err:
            logger.error(f'Failed {msg} - {_err}')

    def __bot_msg(self, msg: MqFatherMessage) -> None:
        _bot_pk: int = msg.params['pk']
        if _bot_pk in self.__BOTS:
            _chat_id: int = msg.params['chat_id']
            _template: str = msg.params['template']
            _text: str = msg.text
            logger.info(f'Bot(pk:{_bot_pk}) sending message to chat_id: {_chat_id}')
            self.__BOTS[_bot_pk].message(_chat_id, _text, _template)
        else:
            logger.warning(f'Bot(pk:{_bot_pk}) not found to send message')

    def __bot_create(self, msg: MqFatherMessage) -> None:
        """ Create and start bot if not created """
        _bot_pk: int = msg.params['pk']
        if self.__bot_remove_if_exist(_bot_pk):
            logger.info(f'Bot(pk:{_bot_pk}) stop and remove to create newone')
        else:
            logger.info(f'Bot(pk:{_bot_pk}) create and run')
        _social = SocialNetwork(msg.params['social'])
        _new_bot: SocialBot = self.__SOCIALS[_social](_bot_pk, msg.params['token'], self.__publish)
        logger.info(f'Bot(pk:{_bot_pk}) created')
        self.__BOTS[_bot_pk] = _new_bot
        self.__BOTS[_bot_pk].start()

    def __bot_delete(self, msg: MqFatherMessage) -> None:
        _bot_pk: int = msg.params['pk']
        if self.__bot_remove_if_exist(_bot_pk):
            logger.info(f'Bot(pk:{_bot_pk}) stopped and removed')
        else:
            logger.warning(f'Bot(pk:{_bot_pk}) not found to delete')

    def __bot_remove_if_exist(self, bot_pk: int) -> bool:
        if bot_pk in self.__BOTS:
            _bot: SocialBot = self.__BOTS.pop(bot_pk)
            _bot.stop()
            return True
        else:
            return False

    def __bot_heartbeat(self, _: MqFatherMessage) -> None:
        _alife_count: int = 0
        _error_count: int = 0
        for _pk, _bot in self.__BOTS.items():
            try:
                _bot.beat()
                _alife_count += 1
            except Exception as _err:
                logger.error(f'Bot(pk:{_pk}) failed heartbeat call  - {_err}')
                _error_count += 1
        logger.info(f'Heartbeat check ended with {_alife_count} alife and {_error_count} bots with errors')
