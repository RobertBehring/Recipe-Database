let amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost:5672', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel){
        if(error1){
            throw error1;
        }
        let queue = 'data';
        channel.assertQueue(queue, {
            durable: false
        });
        channel.prefetch(1);
        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
            channel.consume(queue, function(msg){

                console.log(" [x] Received %s", msg.content.toString());
                let rec = JSON.parse(msg.content);
                let c = rec[0].servings[1] / rec[0].servings[0];
                for(let i = 1; i < rec.length; i++){
                    rec[i].qty *= c;
                }

            channel.sendToQueue(msg.properties.replyTo,
                Buffer.from(JSON.stringify(rec)),{
                    correlationId: msg.properties.correlationId
                });
            channel.ack(msg);
            });
        });
    });