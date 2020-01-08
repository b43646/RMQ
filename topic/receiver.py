import pika


credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("192.168.1.32", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

channel.exchange_declare(exchange="hello-topic-exchange",
                         exchange_type="topic",
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="hello-topic", durable=True, passive=False)
channel.queue_bind(
    queue="hello-topic",
    exchange="hello-topic-exchange",
    routing_key="user.*") # when you change routing key, please don't forget to unbind the queue.


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body.decode("utf-8") == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print("[Received]:" + body.decode("utf-8"))
    return


channel.basic_consume(on_message_callback=msg_consumer,
                      queue="hello-topic",
                      consumer_tag="hello-consumer")

channel.start_consuming()


