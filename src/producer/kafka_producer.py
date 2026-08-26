import json
import time
from kafka import KafkaProducer

from src.generator.event_generator import create_event


# creates one producer connection.
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

minute = 1

for i in range(1, 101):

    # gets an event from generator
    event = create_event(i, minute)

    # sends that event into Kafka.
    producer.send(
        "football-events",
        key=event["match_id"].encode("utf-8"),
        value=event
    )
    print(f"Sent: {event['event_id']}")

    if i % 2 == 0:
        minute += 1

    time.sleep(0.5)

producer.flush()
producer.close()