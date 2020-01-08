import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.32'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body="Hello World"
)

print("[x] Sent 'Hello World!'")

connection.close()

