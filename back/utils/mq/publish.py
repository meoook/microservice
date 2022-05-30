import os
import pika
import logging

from utils.singleton import Singleton

logger = logging.getLogger('mq.publish')


class MqPublish(Singleton):
    def __init__(self):
        _mq_url = os.environ.get('MQ_BROKER_URL', 'amqp://guest:guest@rabbit:5672//')
        logger.info(f'Starting mq connection to publish messages')
        _params = pika.URLParameters(_mq_url)
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange='order', exchange_type='direct')

    def publish(self, body: bytes) -> None:
        self.__channel.basic_publish(exchange='order', routing_key='order.notify', body=body)

    def close(self) -> None:
        self.__connection.close()
