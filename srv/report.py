import pika
import json

from pika import BasicProperties
from pika.spec import Basic
from pika.adapters.blocking_connection import BlockingChannel

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue = channel.queue_declare('order_report')
queue_name = queue.method.queue

channel.queue_bind(
    exchange='order',
    queue=queue_name,
    routing_key='order.report'
)


def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    payload = json.loads(body)
    print(f'''[x] Generating report...
    ID......... {payload['id']}
    Email...... {payload['email']}
    Product.... {payload['product']}
    Quantity... {payload['quantity']}
    ''')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue_name, on_message_callback=callback)

print(f'[x] Waiting for report messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
