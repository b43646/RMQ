import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.199", credentials=credentials)
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

channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key='hola')

conn_broker.close()
