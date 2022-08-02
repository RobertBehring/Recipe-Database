import pika, sys, os
from ingredient_convert import *


# rabbitmq server = "C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5"
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='conversion request')
    channel.queue_declare(queue='conversion delivery')

    def callback(ch, method, properties, body):
        body = body.decode('utf-8')
        print(" [x] Received %r" % body)
        body = conversion(body)
        channel.basic_publish(exchange='',
                              routing_key='conversion delivery',
                              body=json.dumps(body)
                              )
        print(" [x] Sent %r" % body)

    channel.basic_consume(queue='conversion request',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
