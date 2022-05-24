import logging
from typing import Callable
from pika.connection import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties

from bots.src.bot_tg import SocialTelegramBot
from bots.src.objects import BotFatherMessage, SocialBot, SocialName, FatherAction, SocialNames

logger = logging.getLogger('bot.father')


class BotFather:
    """ AMQ Consumer to control bots """

    __SOCIALS: dict[SocialName, Callable] = {
        SocialNames.TG: SocialTelegramBot,
        SocialNames.IN: SocialTelegramBot,
        SocialNames.VK: SocialTelegramBot,
        SocialNames.FB: SocialTelegramBot,
        SocialNames.DC: SocialTelegramBot,
    }
    EXCHANGE: str = 'bot'

    # TODO: Create as singleton
    def __init__(self):
        self.__BOTS: dict[int, SocialBot] = {}
        self.__actions: dict[FatherAction, Callable] = {
            'create': self.__bot_create,
            'delete': self.__bot_delete,
            'beat': self.__bot_heartbeat,
            'msg': self.__bot_msg,
        }

        _params: ConnectionParameters = ConnectionParameters('localhost')
        _connection: BlockingConnection = BlockingConnection(_params)
        self.__channel: BlockingChannel = _connection.channel()

        self.__channel.exchange_declare(exchange=self.EXCHANGE, exchange_type='direct')

        _queue = self.__channel.queue_declare('bot_father')
        _queue_name = _queue.method.queue

        self.__channel.queue_bind(exchange=self.EXCHANGE, queue=_queue_name, routing_key=f'{self.EXCHANGE}.father')
        self.__channel.basic_consume(_queue_name, on_message_callback=self.__callback)

        try:
            logger.warning(f'Start consuming queue "{_queue_name}"')
            self.__channel.start_consuming()
        except Exception as _err:
            logger.warning(f'Channel stop consuming - {_err}')
            self.__channel.stop_consuming()
        _connection.close()

    def __publish(self, body: bytes) -> None:
        """ Function for bots to put message in queue """
        # TODO: routing key variable
        self.__channel.basic_publish(exchange=self.EXCHANGE, routing_key='bot.msg', body=body)

    def __callback(self, ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            _msg: BotFatherMessage = BotFatherMessage.from_bytes(body)
        except Exception as _err:
            logger.error(f'Failed to create message from "{body}" - {_err}')
        else:
            self.__do_action(_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __do_action(self, msg: BotFatherMessage) -> None:
        try:
            self.__actions[msg.action](msg)
        except Exception as _err:
            logger.error(f'Failed to handle message "{msg}" - {_err}')

    def __bot_create(self, msg: BotFatherMessage) -> None:
        """ Create and start bot if not created """
        if msg.pk in self.__BOTS:  # If bot already exist -> stop and remove
            _bot: SocialBot = self.__BOTS[msg.pk]
            logger.info(f'Bot(pk:{msg.pk}) stop and remove to create newone')
            _bot.stop()
            self.__BOTS.pop(msg.pk)
        logger.info(f'Bot(pk:{msg.pk}) create and run')
        _new_bot: SocialBot = self.__SOCIALS[msg.social](msg.pk, msg.message)
        self.__BOTS[msg.pk] = _new_bot
        self.__BOTS[msg.pk].start()

    def __bot_heartbeat(self, _: BotFatherMessage) -> None:
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

    def __bot_delete(self, msg: BotFatherMessage) -> None:
        if msg.pk in self.__BOTS:
            _bot: SocialBot = self.__BOTS.pop(msg.pk)
            _bot.stop()
            logger.info(f'Bot(pk:{msg.pk}) deleted')
        else:
            logger.warning(f'Bot(pk:{msg.pk}) not found to delete')

    def __bot_msg(self, msg: BotFatherMessage) -> None:
        if msg.pk in self.__BOTS:
            _chat_id: int = msg.message['chat_id']
            _text: str = msg.message['text']
            logger.info(f'Bot(pk:{msg.pk}) send message to chat id {_chat_id}')
            self.__BOTS[msg.pk].message(_chat_id, _text)
        else:
            logger.warning(f'Bot(pk:{msg.pk}) not found to send message')
