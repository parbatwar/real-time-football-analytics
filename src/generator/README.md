Event
├── event_id    : str 
├── match_id    : str
├── player_id   : str
├── team_id     : str
├── event_type  : str
├── minute      : int
├── x           : int
├── y           : int
└── timestamp   : datetime

Event Type
├──PASS
├──SHOT
├──GOAL
├──FOUL
├──TACKLE
├──YELLOW_CARD
├──RED_CARD
├──SUBSTITUITION

Match
├── match_id: match_001
├── team_101
│   └── players
└── team_102
    └── players

{
  "event_id": "evt_00001",
  "match_id": "match_001",
  "player_id": "player_007",
  "team_id": "team_101",
  "event_type": "PASS",
  "minute": 23,
  "x": 64,
  "y": 41,
  "timestamp": "2026-08-26T09:30:15"
}

Python Event Generator
        │
        ├── Team
        ├── Player
        ├── Event Type
        ├── Minute
        ├── Location
        └── Timestamp
              │
              ▼
        Football Event
              │
           0.5 sec
              │
              ▼
        Next Event