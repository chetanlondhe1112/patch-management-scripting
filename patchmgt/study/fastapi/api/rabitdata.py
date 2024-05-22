from fastapi import FastAPI, HTTPException
import pika
import json

app = FastAPI()

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'hello'

def consume_from_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    data_list = []
    for method_frame, properties, body in channel.consume(RABBITMQ_QUEUE):
        # Process the message
        message = json.loads(body.decode())
        
        data_list.append(message['data'])

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)
    print(data_list)
    # Cancel the consumer
    channel.cancel()

    # Close the connection
    connection.close()

    return data_list

@app.get("/rabbitmq-data")
def get_rabbitmq_data():
    #try:
    rabbitmq_data = consume_from_rabbitmq()
    print(rabbitmq_data)
    return {"data": rabbitmq_data}
    #except Exception as e:
    #    print("Error fetching data from RabbitMQ:", e)
    #    raise HTTPException(status_code=500, detail="Error fetching data from RabbitMQ")