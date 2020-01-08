import pika


def callback(ch, method, properties, body):
    print("[X] Received %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.32'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)
channel.basic_consume(
    queue='hello',
    auto_ack=True,
    on_message_callback=callback)

print('[*] Waiting for message. Yo exit press CTRL+C')
channel.start_consuming()


