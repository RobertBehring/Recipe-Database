let amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost:5672', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }
        channel.assertQueue('', {
                exclusive: true
        }, function(error2, q){
            if(error2){
                throw error2;
            }
            let correlationId = 'abc';
            let recipe = [
                {"servings":[4,8]},
                {"ingredient":"water", "qty":1, "measure":"cup"},
                {"ingredient":"flour", "qty":2.5, "measure":"cup"},
                {"ingredient":"salt", "qty":.75, "measure":"sp"}];
            let rec = JSON.stringify(recipe);

            console.log(' [x] Requesting conversion of');
            console.log(JSON.parse(rec));

            channel.consume(q.queue, function(msg){
                if(msg.properties.correlationId == correlationId){
                    rec = msg.content.toString();
                    let adjRecipe = JSON.parse(msg.content);
                    console.log(' [.] Received');
                    console.log(adjRecipe);
                    setTimeout(function(){
                        connection.close();
                        process.exit(0)
                    }, 500);
                }
            }, {
                noAck: true
            });
            
            channel.sendToQueue('data',
                Buffer.from(rec),{
                    correlationId: correlationId,
                    replyTo: q.queue
            });
        });
    });
});