# app/kafka_producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Replace with your Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        print(f"Message sent to topic '{topic}': {message}")
    except Exception as e:
        print(f"Error sending message to Kafka: {e}")