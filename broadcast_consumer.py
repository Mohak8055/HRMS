from kafka import KafkaConsumer
import json
import requests

def notify_fastapi(message):
    try:
        requests.post("http://localhost:8000/internal/broadcast", json=message)
        print(f"Notified FastAPI of new message: {message}")
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to FastAPI: {e}")

def broadcast_consumer():
    consumer = KafkaConsumer(
        'broadcast_messages',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='broadcast-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        notify_fastapi(message.value)

if __name__ == "__main__":
    broadcast_consumer()