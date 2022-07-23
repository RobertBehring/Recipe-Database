# !/usr/bin/env python
import json
import pika

data_input = {"Spaghetti": [
    # mass->mass metric
    {"ingredient": "all-purpose flour", "quantity": "100", "measure": "kg", "desired": "g"},
    # mass->mass imperial
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "lb", "desired": "oz"},
    # mass->mass imperial->metric
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "oz", "desired": "g"},
    # mass->mass metric->imperial
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "g", "desired": "oz"},

    # vol->vol metric->imperial
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "ml", "desired": "c"},
    # vol->vol imperial->metric
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "c", "desired": "ml"},
    # vol->vol imperial
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "gal", "desired": "c"},
    # vol->vol mass
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "l", "desired": "ml"},

    # mass->vol metric
    {"ingredient": "all-purpose flour", "quantity": "120", "measure": "g", "desired": "ml"},
    # mass->vol imperial
    {"ingredient": "all-purpose flour", "quantity": "16", "measure": "oz", "desired": "c"},
    # vol->mass imperial->metric
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "c", "desired": "g"},
    # vol->mass metric->imperial
    {"ingredient": "all-purpose flour", "quantity": "1", "measure": "l", "desired": "oz"}
]}

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='unit conversion')

channel.basic_publish(exchange='',
                      routing_key='unit conversion',
                      body=json.dumps(data_input)
                      )
print(" [x] Sent 'Requested data to be converted'")

connection.close()
