import os
import pika
import logging

from utils.enums import MqBotRoute, MqExchange
from utils.singleton import Singleton

logger = logging.getLogger('mq.publish')


class MqPublish(Singleton):
    def __init__(self):
        _mq_url = os.environ.get('MQ_BROKER_URL', 'amqp://guest:guest@rabbit:5672//')
        logger.info(f'Starting mq connection to publish messages')
        _params = pika.URLParameters(_mq_url)
        self.__connection = pika.BlockingConnection(_params)
        self.__channel = self.__connection.channel()
        # TODO: What about exchange
        # self.__channel.exchange_declare(exchange=self.EXCHANGE.value, exchange_type='direct')
        self.__channel.exchange_declare(exchange=MqExchange.BOT.value, exchange_type='direct')

    def publish(self, route: MqBotRoute, body: bytes) -> None:
        logger.debug(f'Publishing to {route.value}')
        # self.__channel.basic_publish(exchange=self.EXCHANGE.value, routing_key=route.value, body=body)
        self.__channel.basic_publish(exchange=MqExchange.BOT.value, routing_key=route.value, body=body)

    def close(self) -> None:
        self.__connection.close()
