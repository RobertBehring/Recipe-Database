# Recipe Database Program :: CS 361 - Software Engineering I

## Program Description

<p>
<strong>The Recipe Database Program provides users a digital solution for storing cooking recipes.</strong> <br/><br/>
This program contains tools to store recipe details including but not limited to: serving sizes, creation dates, ingredient 
details, and a recipe log for step-by-step instructions or to mark progress on your recipe design process. Included also
is functionality for a unit of measurement conversion microservice (detailed below). This microservice provides unit of 
measurement conversion within masses and volumes as well as between masses and volumes for a number of common household 
ingredients. Density conversions are made possible via a dataset from King Arthur Flour's 
<a href="https://www.kingarthurbaking.com/learn/ingredient-weight-chart">Ingredient Weight Chart</a>. Furthermore, 
this microservice is made possible via a pipeline using RabbitMQ.
</p>
<p><strong>A few functions that this program provides on top of the core database feature-set.</strong></p>

- Search for recipe by name
- Recipe serving size conversion provides automatic resizing of ingredient amounts
- Ingredient unit of measurement conversion provides automatic resizing of ingredient amount.
- A detailed help & documentation section to provide users a granular level of detail to learn all the functions this 
program provides.
- An Ingredient Unit of Measurement Microservice using a RabbitMQ pipeline.

## Microservice :: Recipe Ingredient Conversion

### Communication contract

> #### All communications with this microservice are accomplished via the RabbitMQ pipeline.

<details><summary>Microservice description
</summary>
<p></br>
	The <strong>Recipe Ingredient Conversion</strong> microservice is intended to provide users with the ability to convert 
	recipe ingredients from one unit of measurement to another. Users will be able to convert masses and volumes within and
	between the metric and imperial unit system. 

	In order to use this microservice you will need to be able to communicate with it via a RabbitMQ pipeline. You can find
	details on how to request and receive data below. You can also view how data can be sent and received from this 
	micoservice via the UML diagram at the bottom of the README.

</p>
</details>
<details><summary>To <strong>request</strong> data from this microservice:
</summary>
<p>

1. Establish a RabbitMQ pipeline
2. Then declare a queue named 'conversion request'
3. Send your formatted JSON recipe list into this queue

Example call (python3):

```
# Establish RabbitMQ pipeline
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue (conversion request)
channel.queue_declare(queue='conversion request')

# Send your formatted JSON recipe list into the queue w/routing_key == queue
channel.basic_publish(exchange='',
                      routing_key='conversion request',
                      body=data_input
                      )
```

All JSON data sent into the queue must be formatted as follows:

```
{"Recipe name": [
    {"ingredient": "string", "quantity": "number", "measure": "string", "desired": "string"}
]}
```

Example:

```
{"Spaghetti": [
    {"ingredient": "all-purpose flour", "quantity": "120", "measure": "g", "desired": "oz"},
    {"ingredient": "table salt", "quantity": "12", "measure": "g", "desired": "oz"},
    {"ingredient": "large egg", "quantity": "2", "measure": "g", "desired": "mg"}
]}
```

Ingredient names must belong to this list:

```
ingredients = ['all-purpose flour', 'baking powder', 'baking soda', 'bread flour', 'brown sugar', 'butter', 'carrots', 'celery', 'feta cheese', 'cheddar cheese', 'cherries', 'chocolate chips', 'cocoa', 'coconut', 'corn syrup', 'cranberries', 'cream', 'cream cheese', 'creme fraiche', 'dates', 'dried milk', 'potato flakes', 'large egg', 'figs', 'flax meal', 'minced garlic', 'peeled garlic', 'ghee', 'gluten-free all-purpose flour', 'granola', 'hazelnuts', 'honey', 'jam', 'preserves', 'lard', 'leeks', 'lemon juice', 'macadamia nuts', 'maple syrup', 'marshmallow spread', 'mini marshmallows', 'marzipan', 'masa harina', 'mascarpone cheese', 'mayonnaise', 'evaporated milk', 'milk', 'molasses', 'mushrooms', 'oat flour', 'old fashioned oats', 'olive oil', 'olives', 'onions', 'paleo baking flour', 'palm shortening', 'pastry flour', 'peaches', 'peanut butter', 'peanuts', 'pears', 'pecans', 'pine nuts', 'pineapple', 'pistachio nuts', 'pizza sauce', 'poppy seeds', 'quinoa', 'raisins', 'raspberries', 'rhubarb', 'rice', 'table salt', 'semolina flour', 'sesame seeds', 'sour cream', 'sourdough starter', 'steel cut oats', 'strawberries', 'white sugar', 'sweetened condensed milk', 'tahini', 'tapioca flour', 'tomato paste', 'turbinado sugar', 'vanilla extract', 'vegetable oil', 'vegetable shortening', 'walnuts', 'water', 'instant yeast', 'yogurt', 'zucchini']
```

Units of measurement must belong to one of these three lists:

> **Note**: all units are abbreviated per convention

```
metric_masses = ["mg", "g", "kg"]
metric_volumes = ["ml", "l", "kl"]
imperial_masses = ["oz", "lb"]
imperial_volumes = ["tsp", "tbsp", "fl oz", "c", "pt", "qt", "gal"]
```

</p>
</details>

<details><summary>To <strong>receive</strong> data from this microservice:
</summary>
<p>

1. Establish a RabbitMQ pipeline
2. Then declare a queue named 'conversion delivery'
3. Set up a basic consume on queue='conversion delivery'
4. Create a callback function to receive and decode your converted data

Example call (python3):

```
def main():
    # Establish RabbitMQ pipeline
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue (conversion delivery)
    channel.queue_declare(queue='conversion delivery')

    # Callback function handles how you want to receive the data
    def callback(ch, method, properties, body):
        body = body.decode('utf-8')
        print(" [x] Received %r" % body)

    # Look for data within queue='conversion delivery'
    channel.basic_consume(queue='conversion delivery',
                          auto_ack=True,
                          on_message_callback=callback)

    # provide user feedback on program execution
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # consume data from queue='conversion delivery' until user quits program
    channel.start_consuming()


# run the basic_consume() on queue='conversion delivery' until the user exits the program
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
```

All JSON data received from the delivery queue will be formatted as follows:

> **Note**: amounts will be rounded to six decimal places when possible

```
{'converted recipe name': [ {'ingredient': 'string', 'quantity': 'number', 'measure': 'string'} ]}
```

Example:

```
{'Spaghetti': [    
	{'ingredient': 'all-purpose flour', 'quantity': '4.232804', 'measure': 'oz'}, 
	{'ingredient': 'table salt', 'quantity': '0.42328', 'measure': 'oz'}, 
	{'ingredient': 'large egg', 'quantity': '2000.0', 'measure': 'mg'}
]}
```

</p>
</details>

<details><summary>UML Diagram
</summary></br>

![Ingredient conversion microservice UML](https://user-images.githubusercontent.com/91280849/180588469-0de16d88-2d70-4e2e-afa6-d445f4dbca14.png)

</details>
