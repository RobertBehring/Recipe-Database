import pika, sys, os
from ingredient_convert import *


# rabbitmq server = "C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5"
def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='unit conversion')

    def callback(ch, method, properties, body):
        body = body.decode('utf-8')
        body = conversion(body)
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='unit conversion',
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
