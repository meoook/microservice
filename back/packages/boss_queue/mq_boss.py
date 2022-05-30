import logging
from typing import Callable
from pika.connection import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties

from packages.boss_queue.mq_object import MqBotBossMessage
from utils.enums import MqAction, MqExchange, MqBotRoute, MsgTemplate

logger = logging.getLogger('bot.boss')


class MqBotBossConsumer:
    """ AMQ Consumer for `boss` server """

    EXCHANGE = MqExchange.BOT
    QUEUE: str = 'boss'

    def __init__(self, mq_url: str):
        if not mq_url or not isinstance(mq_url, str):
            raise ValueError('need mq_url to start consuming')
        self.__actions: dict[MqAction, Callable[[MqBotBossMessage], None]] = {
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

        self.__channel.queue_bind(exchange=self.EXCHANGE.value, queue=_queue_name, routing_key=MqBotRoute.BOSS.value)
        self.__channel.basic_consume(_queue_name, on_message_callback=self.__callback)

        try:
            logger.info(f'Start consuming queue "{_queue_name}"')
            self.__channel.start_consuming()
        except Exception as _err:
            logger.warning(f'Stop consuming queue "{_queue_name}" - {_err}')
            self.__channel.stop_consuming()
        _connection.close()

    def __publish_to_father(self, body: bytes) -> None:
        """ Function for bots to put message in queue """
        self.__channel.basic_publish(exchange=self.EXCHANGE.value, routing_key=MqBotRoute.FATHER.value, body=body)

    def __callback(self, ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            _msg: MqBotBossMessage = MqBotBossMessage.from_bytes(body)
        except Exception as _err:
            logger.error(f'Failed to create message from "{body}" - {_err}')
        else:
            self.__do_action(_msg)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __do_action(self, msg: MqBotBossMessage) -> None:
        try:
            self.__actions[msg.action](msg)
        except Exception as _err:
            logger.error(f'Failed to handle message "{msg}" - {_err}')
