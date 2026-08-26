import json
from kafka import KafkaProducer

event = {
    "event_id": "evt_00001",
    "match_id": "match_001",
    "player_id": "player_014",
    "team_id": "team02",
    "event_type": "SHOT",
    "minute": 1,
    "x": 14,
    "y": 42,
    "timestamp": "2026-08-26T12:07:54"
}

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send(
    "football-events",
    value=event
)

producer.flush()


print("Message sent!")