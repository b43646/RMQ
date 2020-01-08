import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)

channel.queue_declare(queue="hello-queue", durable=True, passive=False)

msg = "Hello"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props.delivery_mode = 2


# Send a message
try:
    channel.basic_publish(exchange='hello-exchange',
                          routing_key='hola',
                          body=msg,
                          properties=pika.BasicProperties(content_type='text/plain',
                                                          delivery_mode=1),
                          mandatory=True)
    print('Message was published')
except pika.exceptions.UnroutableError:
    print('Message was returned')

conn_broker.close()
