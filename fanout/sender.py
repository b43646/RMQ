import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()
channel.exchange_declare(
    exchange="hello-fanout-exchange",
    exchange_type="fanout",
    passive=False,
    durable=True,
    auto_delete=False)

channel.queue_declare(queue="hello-fanout", durable=True, passive=False)

msg = "Hello"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props.delivery_mode = 2
msg_props.expiration = "10000"
# a = dict()
# a["a"] = 123
# msg_props.headers=a
channel.basic_publish(
    body=msg,
    exchange="hello-fanout-exchange",
    properties=msg_props,
    routing_key='AXXX')

conn_broker.close()
