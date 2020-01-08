import pika


credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="hello-exchange",
                         exchange_type="direct",
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="hello-queue", durable=True, passive=False)
channel.queue_bind(
    queue="hello-queue",
    exchange="hello-exchange",
    routing_key="hola")


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body.decode("utf-8") == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print("[Received]:" + body.decode("utf-8"))
    return


channel.basic_qos(0, 3, False)
channel.basic_consume(on_message_callback=msg_consumer,
                      queue="hello-queue",
                      consumer_tag="hello-consumer",
                      auto_ack=False)

channel.start_consuming()


