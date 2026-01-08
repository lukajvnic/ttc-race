import api
import json
from confluent_kafka import Producer
from constants import *


def delivery_callback(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_to_kafka(topic, data, bootstrap_servers=BROKER):
    """
    Produces a single JSON message to the specified Kafka topic.
    """
    try:
        producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'socket.timeout.ms': 10000
        })
        
        producer.produce(
            topic,
            value=json.dumps(data).encode('utf-8'),
            callback=delivery_callback
        )
        producer.flush(timeout=30)
        print(f"Successfully produced to {topic}")
        
    except Exception as e:
        print(f"Failed to produce message: {e}")


if __name__ == "__main__":
    print("fetching data...")
    test_data = api.get_leaderboard()
    print("producing data...")
    produce_to_kafka(topic=TOPIC, data=test_data)
    print("done!")
