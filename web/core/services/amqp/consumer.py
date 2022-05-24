import logging
import json
from pika.connection import ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties

from web.core.services.amqp.publisher import AmqpPublish

logger = logging.getLogger(__name__)


class AmqpConsumer:
    def __init__(self):
        _params: ConnectionParameters = ConnectionParameters('localhost')
        _connection: BlockingConnection = BlockingConnection(_params)
        _channel: BlockingChannel = _connection.channel()

        _queue = _channel.queue_declare('order_report')
        _queue_name = _queue.method.queue
        _exchange_name = AmqpPublish.EXCHANGE

        _channel.queue_bind(exchange=_exchange_name, queue=_queue_name, routing_key=f'{_exchange_name}.msg')
        _channel.basic_consume(_queue_name, on_message_callback=self.callback)

        print(f'[x] Waiting for report messages. To exit press CTRL+C')

        try:
            _channel.start_consuming()
        except KeyboardInterrupt:
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
