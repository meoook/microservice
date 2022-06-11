from typing import Callable
from pika.connection import URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties
from utils.enums import MqExchange, MqBotRoute


class MqConsumer:
    """ AMQ Consumer """

    def __init__(self, mq_url: str, exchange: MqExchange, queue: str, route: MqBotRoute):
        if not mq_url or not isinstance(mq_url, str):
            raise ValueError('need mq_url to start consuming')
        if not queue or not isinstance(queue, str):
            raise ValueError('need to set queue for consumer')
        self.EXCHANGE: MqExchange = exchange
        self.QUEUE: str = queue

        _params: URLParameters = URLParameters(mq_url)
        _params.socket_timeout = 5
        self.__connection: BlockingConnection = BlockingConnection(_params)
        self.__channel: BlockingChannel = self.__connection.channel()
        self.__channel.exchange_declare(exchange=self.EXCHANGE.value, exchange_type='direct')

        _queue = self.__channel.queue_declare(self.QUEUE)
        self.__queue = _queue.method.queue

        self.__channel.queue_bind(exchange=self.EXCHANGE.value, queue=self.__queue, routing_key=route.value)

    def _start(self, callback: Callable[[BlockingChannel, Basic.Deliver, BasicProperties, bytes], None]):
        self.__channel.basic_consume(self.__queue, on_message_callback=callback)
        try:
            self.__channel.start_consuming()
        except Exception as _err:
            self.__channel.stop_consuming()
            self.__connection.close()
            raise _err

    def _publish(self, route: MqBotRoute,  body: bytes) -> None:
        """ Function put message in queue """
        self.__channel.basic_publish(exchange=self.EXCHANGE.value, routing_key=route.value, body=body)
