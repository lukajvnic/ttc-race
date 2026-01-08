from confluent_kafka import Consumer
import json
from constants import *

# Create a Kafka consumer
consumer = Consumer({
    'bootstrap.servers': BROKER,
    'group.id': 'test-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([TOPIC])

print(f"Listening for messages on topic '{TOPIC}'...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
            
        value = json.loads(msg.value().decode('utf-8'))
        print(f"Topic: {msg.topic()}")
        print(f"Partition: {msg.partition()}")
        print(f"Offset: {msg.offset()}")
        print(f"Value: {value}")
        print("-" * 50)

except KeyboardInterrupt:
    print("Shutting down...")
finally:
    consumer.close()
