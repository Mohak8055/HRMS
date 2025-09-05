from kafka import KafkaConsumer
import json
import asyncio
from app.websocket_manager import manager

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
        asyncio.run(manager.broadcast(json.dumps(message.value)))

if __name__ == "__main__":
    broadcast_consumer()