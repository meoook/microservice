import pika
import json
import uuid


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='order',
    exchange_type='direct'
)

order = {
    'id': f'{uuid.uuid4()}',
    'email': 'john@game.ru',
    'product': 'Jacket',
    'quantity': 1
}

channel.basic_publish(exchange='order', routing_key='order.notify', body=json.dumps({'email': order['email']}).encode())

print('[x] Send notify message')

channel.basic_publish(exchange='order', routing_key='order.report', body=json.dumps(order).encode())

print('[x] Send report message')

connection.close()
