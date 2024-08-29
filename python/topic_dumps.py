from confluent_kafka import Consumer
import json
from json import dumps

####
# Sample code to dump a topic to the console
# Each table is a separate topic
#####

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'testing12345',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': 'false'
})

# Subscribe to topics for
# the customers, products, and products_on_hand tables
c.subscribe(['dbserver1.inventory.customers','dbserver1.inventory.products','dbserver1.inventory.products_on_hand'])


try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
            print("Waiting... ctrl-c to stop....")
        elif msg.error():
            print("ERROR: %s".format(msg.error()))
        #elif msg.value() is not None:    
        else:
           # A message has arrived
        
            if(msg.value()):
                # decode the message, kafka sends bytes
                key = msg.key().decode('utf-8')
                value = msg.value().decode('utf-8')
                
                # extract offset and timestamp
                offset = msg.offset()
                timestamp = msg.timestamp() 
                
               
                table_id = json.loads(value)['payload']['source']['table']
                db_id = json.loads(value)['payload']['source']['db']
               

    
                print("\nGOT AN EVENT\n")
                print(f"Kafka topic: {msg.topic()}")
                print(f"key: \n {key}")
                print(f"value: \n {value}")
               
                            
except KeyboardInterrupt:
    pass
finally:
        # Leave group and commit final offsets
        c.close()

