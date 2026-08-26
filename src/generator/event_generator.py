import random
import time
from datetime import datetime


teams = {
    "team01" : [
        "player_001",
        "player_002",
        "player_003",
        "player_004",
        "player_005",
        "player_006",
        "player_007",
        "player_008",
        "player_009",
        "player_010",
        "player_011"
    ], 
    "team02" : [
        "player_012",
        "player_013",
        "player_014",
        "player_015",
        "player_016",
        "player_017",
        "player_018",
        "player_019",
        "player_020",
        "player_021",
        "player_022"
    ]
}

event_types = [
    "PASS",
    "SHOT",
    "GOAL",
    "FOUL",
    "TACKLE",
    "YELLOW_CARD",
    "RED_CARD",
    "SUBSTITUTION"
]
event_weights = [60, 12, 10, 8, 2, 5, 1, 2]
EVENT_INTERVAL = 0.5  # seconds

def create_event(event_number, minute):

    team = random.choice(list(teams.keys()))
    player = random.choice(teams[team])

    event = {
        "event_id": f"evt_{event_number:05d}",
        "match_id": "match_001",
        "player_id": player,
        "team_id": team,
        "event_type": random.choices(event_types, weights=event_weights, k=1)[0],
        "minute": minute,
        "x": random.randint(0, 100),
        "y": random.randint(0, 100),
        "timestamp": datetime.now().isoformat()
    }

    return event

minute = 1

for i in range(1, 101):
    event = create_event(i, minute)
    print(event)

    if i % 2 == 0:
        minute += 1

    time.sleep(EVENT_INTERVAL)