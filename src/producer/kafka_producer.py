import json
import random
import time

import psycopg2

from kafka import KafkaProducer

from src.generator.event_generator import (
    create_match,
    create_event,
    teams,
)


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="football_db",
        user="postgres",
        password="postgres",
    )


# ==================================================
# FIND NEXT MATCH NUMBER
# ==================================================

def get_next_match_number():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COALESCE(
                MAX(
                    CAST(
                        REPLACE(
                            match_id,
                            'match_',
                            ''
                        )
                        AS INTEGER
                    )
                ),
                0
            )
        FROM matches
        WHERE match_id LIKE 'match_%';
        """
    )

    max_match_number = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return max_match_number + 1


# ==================================================
# KAFKA PRODUCER
# ==================================================

producer = KafkaProducer(
    bootstrap_servers=[
        "localhost:9092"
    ],

    value_serializer=lambda value: (
        json.dumps(value)
        .encode("utf-8")
    ),

    key_serializer=lambda key: (
        key.encode("utf-8")
    ),
)


# ==================================================
# GET NEXT MATCH NUMBER
# ==================================================

start_match_number = get_next_match_number()


print()
print("=" * 70)
print("                  MATCH GENERATOR")
print("=" * 70)

print(
    f"Next match numbers: "
    f"{start_match_number} and "
    f"{start_match_number + 1}"
)

print("=" * 70)
print()


# ==================================================
# RANDOM TEAM SELECTION
# ==================================================

available_teams = list(
    teams.keys()
)

random.shuffle(
    available_teams
)


# ==================================================
# CREATE TWO RANDOM MATCHES
# ==================================================
#
# Example:
#
# Barcelona vs Chelsea
# Liverpool vs Bayern Munich
#
# All four teams are used exactly once per run.
#
# ==================================================

match_1 = create_match(
    start_match_number,
    available_teams[0],
    available_teams[1],
)

match_2 = create_match(
    start_match_number + 1,
    available_teams[2],
    available_teams[3],
)


# ==================================================
# ASSIGN MATCHES TO KAFKA PARTITIONS
# ==================================================

matches = [
    (
        match_1,
        0,
    ),

    (
        match_2,
        1,
    ),
]


# ==================================================
# DISPLAY MATCHES
# ==================================================

print()
print("=" * 70)
print("               KAFKA FOOTBALL PRODUCER")
print("=" * 70)

for match, partition in matches:
    print(
        f"{match['match_id']} | "
        f"{match['home_team']} "
        f"vs "
        f"{match['away_team']} "
        f"→ Partition {partition}"
    )

print("=" * 70)
print()


# ==================================================
# GLOBAL EVENT NUMBER FOR THIS RUN
# ==================================================

event_number = 1


# ==================================================
# GENERATE LIVE MATCH EVENTS
# ==================================================

for minute in range(
    1,
    91,
):

    print()
    print(
        f"================== MINUTE {minute} =================="
    )

    # ------------------------------------------------
    # Process both matches each minute
    # ------------------------------------------------

    for match, partition in matches:

        match["current_minute"] = minute

        # --------------------------------------------
        # Generate 1 or 2 events for this match
        # --------------------------------------------

        number_of_events = random.choice(
            [
                1,
                2,
            ]
        )

        for _ in range(
            number_of_events
        ):

            event = create_event(
                event_number,
                match,
                minute,
            )

            # ----------------------------------------
            # SEND EVENT TO KAFKA
            # ----------------------------------------

            producer.send(
                topic="football-events",
                partition=partition,
                key=match["match_id"],
                value=event,
            )

            # ----------------------------------------
            # PRINT EVENT
            # ----------------------------------------

            print(
                f"{match['match_id']} | "
                f"{minute:02d}' | "
                f"{event['team']:<15} | "
                f"{event['player']:<20} | "
                f"{event['event_type']:<18} | "
                f"{event['event_id']} | "
                f"Partition {partition}"
            )

            event_number += 1

    # ------------------------------------------------
    # Push messages immediately
    # ------------------------------------------------

    producer.flush()

    # ------------------------------------------------
    # 1 real second = 1 football minute
    # ------------------------------------------------

    time.sleep(1)


# ==================================================
# FINISH MATCHES
# ==================================================

for match, _ in matches:
    match["status"] = "FINISHED"


# ==================================================
# CLOSE PRODUCER
# ==================================================

producer.flush()
producer.close()


# ==================================================
# FINISH MESSAGE
# ==================================================

print()
print("=" * 70)
print("                  PRODUCER FINISHED")
print("=" * 70)

for match, partition in matches:
    print(
        f"{match['match_id']} | "
        f"{match['home_team']} "
        f"vs "
        f"{match['away_team']} "
        f"→ Partition {partition}"
    )

print("=" * 70)