import logging
import json
from pika.connection import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties

from ..amqp.publisher import AmqpPublish
from bots.src.objects import BotCreateParams

logger = logging.getLogger('bot.father')


class BotFather:
    # TODO: Create as singleton
    def __init__(self):
        self.__bots: dict[str, any] = {}
        self.__log: str = '[amqp.bot.father]'

        _params: ConnectionParameters = ConnectionParameters('localhost')
        _connection: BlockingConnection = BlockingConnection(_params)
        _channel: BlockingChannel = _connection.channel()

        _queue = _channel.queue_declare('bot_father')
        _queue_name = _queue.method.queue
        _exchange_name = AmqpPublish.EXCHANGE

        _channel.queue_bind(exchange=_exchange_name, queue=_queue_name, routing_key=f'{_exchange_name}.father')
        _channel.basic_consume(_queue_name, on_message_callback=self.callback)

        print(f'[x] Waiting for report messages. To exit press CTRL+C')

        try:
            _channel.start_consuming()
        except Exception as _err:
            logger.warning(f'{self.__log} channel stop consuming - {_err}')
            _channel.stop_consuming()
        _connection.close()

    @staticmethod
    def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        payload = json.loads(body)
        print(f'''[x] Generating report...
        ID......... {payload['id']}
        Email...... {payload['email']}
        Product.... {payload['product']}
        Quantity... {payload['quantity']}
        ''')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __bot_create(self):
        pass

    def __bot_heartbeat(self):
        pass

    def __bot_delete(self):
        pass

    def __bot_msg(self):
        pass

    def __serialize_create_params(self, params: BotCreateParams):
        pass
