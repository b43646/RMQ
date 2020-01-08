import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel.exchange_declare(
    exchange="hello-topic-exchange",
    exchange_type="topic",
    passive=False,
    durable=True,
    auto_delete=False)

channel.queue_declare(queue="hello-topic", durable=True, passive=False)

msg = "Hello"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props.delivery_mode = 2

channel.basic_publish(
    body="hello 1.1",
    exchange="hello-topic-exchange",
    properties=msg_props,
    routing_key='user.1.1')

channel.basic_publish(
    body="hello 2",
    exchange="hello-topic-exchange",
    properties=msg_props,
    routing_key='user.2')

channel.basic_publish(
    body="hello 3",
    exchange="hello-topic-exchange",
    properties=msg_props,
    routing_key='user.3')

conn_broker.close()
