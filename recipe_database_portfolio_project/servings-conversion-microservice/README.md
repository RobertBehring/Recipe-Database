# Conversion-Microservice

This microservice functionality is based on the RabbitMQ tutorial for Remote Process Calls (RPC) linked below
https://www.rabbitmq.com/tutorials/tutorial-six-python.html

**Requesting Data**
1) Create RabbitMQ connection
2) Generate unqueId
3) Format recipe as JSON array of objects as described below
4) Stringify JSON recipe
5) Create generic queue to listen for response from microservice
6) Send formatted recipe string and uniqueId to queue named 'data' to be passed asynchronously to the microservice. Specify that the microservice should **replyTo:** the generic listening queue

**Data Formatting**

recipe = [
                {"servings":[4,8]},
                {"ingredient":"water", "qty":1, "measure":"cup"},
                {"ingredient":"flour", "qty":2.5, "measure":"cup"},
                {"ingredient":"salt", "qty":.75, "measure":"sp"}];

1) Array element [0] must be object key named "servings" whose value is an array where element [0] is the original serving size and element [1] is the desired new serving size
2) Subsequent elements in the recipe array must be objects of three key:value pairs. **The second key:value pair must be a key named "qty" and have a numeric value equal to the recipe quantity of ingredient desired to be adjusted**

**Receiving Data**
1) On the generic listening queue specified in the **replyTo:**, verify uniqueId matches the message sent to the 'data' queue
2) Record the message content string as a variable
3) JSON.parse the reply message to access the converted recipe quantities. For example, if the reply message was parsed and saved as a variable reply, then the adjusted quanitities would be accessed with the following javaScript code:

**for(let i = 1; i < reply.length; i++)  reply[i].qty;**


RabbitMQ allows the data and replyTo: queues to stay open so long as a reply has not been recieved, and terminates both upon receipt of the reply as illustrated in the below diagram

![image](https://user-images.githubusercontent.com/107817113/180894350-737eae6e-c610-47dc-90bb-edafa13ea869.png)

