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

args = dict()
args["x-dead-letter-exchange"] = "dlx.exchange"
channel.queue_declare(queue="hello-queue2", durable=True, passive=False, arguments=args)

msg = "Hello"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_props.delivery_mode = 2
msg_props.expiration = "10000"

channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key='hola2')

conn_broker.close()
