import pika
import datetime as dt
import time
import json
# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')
channel.queue_declare(queue='chetan_hello')


# Publish a message

while 1:
    tm=dt.datetime.today().now()
    remark="rabit working"

    data={'time':str(tm),'remark':remark}
    data=json.dumps(data)

    channel.basic_publish(exchange='', routing_key='hello', body=data)
    print("-"*20)
    print(f" [{tm}] Sent \n\t 'Hello,your data [{data}]'")
    time.sleep(5)

# Close connection
#connection.close()