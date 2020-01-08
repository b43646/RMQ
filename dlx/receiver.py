import pika


credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="hello-exchange2",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)
args = dict()
args["x-dead-letter-exchange"] = "dlx.exchange"
channel.queue_declare(queue="hello-queue2", durable=True, passive=False, arguments=args)
channel.queue_bind(
    queue="hello-queue2",
    exchange="hello-exchange",
    routing_key="hola2")

# 声明死信队列

channel.exchange_declare(exchange="dlx.exchange",
                         exchange_type="topic",
                         passive=False,
                         durable=True,
                         auto_delete=False)
channel.queue_declare(queue="dlx.queue", durable=True, passive=False)
channel.queue_bind(
    queue="dlx.queue",
    exchange="dlx.exchange",
    routing_key="#")


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body.decode("utf-8") == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer2")
        channel.stop_consuming()
    else:
        print("[Received]:" + body.decode("utf-8"))
    return


channel.basic_consume(on_message_callback=msg_consumer,
                      queue="hello-queue2",
                      consumer_tag="hello-consumer2")

channel.start_consuming()


