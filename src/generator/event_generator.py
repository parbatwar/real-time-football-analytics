import random
from datetime import datetime


matches = {
    "match_001": {
        "team01": [
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
        "team02": [
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
    },

    "match_002": {
        "team03": [
            "player_023",
            "player_024",
            "player_025",
            "player_026",
            "player_027",
            "player_028",
            "player_029",
            "player_030",
            "player_031",
            "player_032",
            "player_033"
        ],
        "team04": [
            "player_034",
            "player_035",
            "player_036",
            "player_037",
            "player_038",
            "player_039",
            "player_040",
            "player_041",
            "player_042",
            "player_043",
            "player_044"
        ]
    },

    "match_003": {
        "team05": [
            "player_045",
            "player_046",
            "player_047",
            "player_048",
            "player_049",
            "player_050",
            "player_051",
            "player_052",
            "player_053",
            "player_054",
            "player_055"
        ],
        "team06": [
            "player_056",
            "player_057",
            "player_058",
            "player_059",
            "player_060",
            "player_061",
            "player_062",
            "player_063",
            "player_064",
            "player_065",
            "player_066"
        ]
    },

    "match_004": {
        "team07": [
            "player_067",
            "player_068",
            "player_069",
            "player_070",
            "player_071",
            "player_072",
            "player_073",
            "player_074",
            "player_075",
            "player_076",
            "player_077"
        ],
        "team08": [
            "player_078",
            "player_079",
            "player_080",
            "player_081",
            "player_082",
            "player_083",
            "player_084",
            "player_085",
            "player_086",
            "player_087",
            "player_088"
        ]
    },

    "match_005": {
        "team09": [
            "player_089",
            "player_090",
            "player_091",
            "player_092",
            "player_093",
            "player_094",
            "player_095",
            "player_096",
            "player_097",
            "player_098",
            "player_099"
        ],
        "team10": [
            "player_100",
            "player_101",
            "player_102",
            "player_103",
            "player_104",
            "player_105",
            "player_106",
            "player_107",
            "player_108",
            "player_109",
            "player_110"
        ]
    }
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


event_weights = [
    60,  # PASS
    12,  # SHOT
    10,  # GOAL
    8,   # FOUL
    2,   # TACKLE
    5,   # YELLOW_CARD
    1,   # RED_CARD
    2    # SUBSTITUTION
]


def create_event(event_number, minute):

    # Select a match
    match_id = random.choice(list(matches.keys()))

    # Select a team from that match
    teams = matches[match_id]
    team_id = random.choice(list(teams.keys()))

    # Select a player from that team
    player_id = random.choice(teams[team_id])

    # Select event type using realistic weights
    event_type = random.choices(
        event_types,
        weights=event_weights,
        k=1
    )[0]

    event = {
        "event_id": f"evt_{event_number:05d}",
        "match_id": match_id,
        "player_id": player_id,
        "team_id": team_id,
        "event_type": event_type,
        "minute": minute,
        "x": random.randint(0, 100),
        "y": random.randint(0, 100),
        "timestamp": datetime.now().isoformat()
    }

    return event