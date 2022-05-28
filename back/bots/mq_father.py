import logging
from typing import Callable
from pika.connection import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties
from utils.enums import SocialName, MqAction, MqExchange, MqBotRoute, MsgTemplate
from .mq_object import MqFatherMessage
from .socials.bot_object import SocialBot
from .socials.bot_tg import SocialTelegramBot

logger = logging.getLogger('bot.father')


class BotFather:
    """ AMQ Consumer to control bots """

    EXCHANGE = MqExchange.BOT
    QUEUE: str = 'bot_father'
    __SOCIALS: dict[SocialName, Callable[[int, str], SocialBot]] = {
        SocialName.TELEGRAM: SocialTelegramBot,
        SocialName.INSTAGRAM: SocialTelegramBot,
        SocialName.VKONTAKTE: SocialTelegramBot,
        SocialName.FACEBOOK: SocialTelegramBot,
        SocialName.DISCORD: SocialTelegramBot,
    }

    def __init__(self, mq_url: str):
        if not mq_url or not isinstance(mq_url, str):
            raise ValueError('need mq_url to start consuming')
        self.__BOTS: dict[int, SocialBot] = {}
        self.__actions: dict[MqAction, Callable[[MqFatherMessage], None]] = {
            MqAction.CREATE: self.__bot_create,
            MqAction.DELETE: self.__bot_delete,
            MqAction.BEAT: self.__bot_heartbeat,
            MqAction.MSG: self.__bot_msg,
        }

        _params: URLParameters = URLParameters(mq_url)
        _params.socket_timeout = 5
        _connection: BlockingConnection = BlockingConnection(_params)
        self.__channel: BlockingChannel = _connection.channel()
        self.__channel.exchange_declare(exchange=self.EXCHANGE.value, exchange_type='direct')

        _queue = self.__channel.queue_declare(self.QUEUE)
        _queue_name = _queue.method.queue

        self.__channel.queue_bind(exchange=self.EXCHANGE.value, queue=_queue_name, routing_key=MqBotRoute.FATHER.value)
        self.__channel.basic_consume(_queue_name, on_message_callback=self.__callback)

        try:
            logger.info(f'Start consuming queue "{_queue_name}"')
            self.__channel.start_consuming()
        except Exception as _err:
            logger.warning(f'Stop consuming queue "{_queue_name}" - {_err}')
            self.__channel.stop_consuming()
        _connection.close()

    def __publish(self, body: bytes) -> None:
        """ Function for bots to put message in queue """
        self.__channel.basic_publish(exchange=self.EXCHANGE.value, routing_key=MqBotRoute.BOSS.value, body=body)

    def __callback(self, ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
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
            logger.error(f'Failed to handle message "{msg}" - {_err}')

    def __bot_create(self, msg: MqFatherMessage) -> None:
        """ Create and start bot if not created """
        _bot_pk: int = msg.params.pk
        if _bot_pk in self.__BOTS:  # If bot already exist -> stop and remove
            _bot: SocialBot = self.__BOTS[_bot_pk]
            logger.info(f'Bot(pk:{_bot_pk}) stop and remove to create newone')
            _bot.stop()
            self.__BOTS.pop(_bot_pk)
        logger.info(f'Bot(pk:{_bot_pk}) create and run')
        _new_bot: SocialBot = self.__SOCIALS[msg.params.social](_bot_pk, msg.params.token)
        self.__BOTS[_bot_pk] = _new_bot
        self.__BOTS[_bot_pk].start()

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

    def __bot_delete(self, msg: MqFatherMessage) -> None:
        _bot_pk: int = msg.params.pk
        if _bot_pk in self.__BOTS:
            _bot: SocialBot = self.__BOTS.pop(_bot_pk)
            _bot.stop()
            logger.info(f'Bot(pk:{_bot_pk}) deleted')
        else:
            logger.warning(f'Bot(pk:{_bot_pk}) not found to delete')

    def __bot_msg(self, msg: MqFatherMessage) -> None:
        _bot_pk: int = msg.params.pk
        if _bot_pk in self.__BOTS:
            _chat_id: int = msg.params.chat_id
            _template: MsgTemplate = msg.params.template
            _text: str = msg.text
            logger.info(f'Bot(pk:{_bot_pk}) sending message to chat_id: {_chat_id}')
            self.__BOTS[_bot_pk].message(_chat_id, _text)
        else:
            logger.warning(f'Bot(pk:{_bot_pk}) not found to send message')
