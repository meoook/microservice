import json
import logging
from pika.connection import ConnectionParameters, URLParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

logger = logging.getLogger(__name__)


class AmqpPublish:
    EXCHANGE: str = 'bot'

    @classmethod
    def publish(cls, route: str, msg: any):
        _params: ConnectionParameters = ConnectionParameters('localhost')
        _connection: BlockingConnection = BlockingConnection(_params)
        _channel: BlockingChannel = _connection.channel()

        _channel.exchange_declare(exchange=cls.EXCHANGE, exchange_type='direct')

        _body: bytes = json.dumps(msg).encode()
        _route: str = f'{cls.EXCHANGE}.{route}' if route else cls.EXCHANGE
        logger.info(f'[amqp] Publish exchange `{cls.EXCHANGE}` route: {_route}')
        _channel.basic_publish(exchange=cls.EXCHANGE, routing_key=_route, body=_body)
        _connection.close()
