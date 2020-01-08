import pika


credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="hello-fanout-exchange",
                         exchange_type="fanout",
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="hello-fanout", durable=True, passive=False)
channel.queue_bind(
    queue="hello-fanout",
    exchange="hello-fanout-exchange",
    routing_key="")


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body.decode("utf-8") == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print("[Received]:" + body.decode("utf-8"))
    return


channel.basic_consume(on_message_callback=msg_consumer,
                      queue="hello-fanout",
                      consumer_tag="hello-consumer")

channel.start_consuming()


