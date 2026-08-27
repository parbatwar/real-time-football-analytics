import random
import time
from datetime import datetime


# ==================================================
# TEAMS AND PLAYERS
# ==================================================

teams = {

    "Chelsea": [
        "Sanchez",
        "James",
        "Lacroix",
        "Colwill",
        "Cucurella",
        "Caicedo",
        "Enzo Fernandez",
        "Palmer",
        "Rogers",
        "Joao Pedro",
        "Neto",
    ],

    "Liverpool": [
        "Alisson",
        "Alexander-Arnold",
        "Van Dijk",
        "Konate",
        "Robertson",
        "Mac Allister",
        "Gravenberch",
        "Szoboszlai",
        "Salah",
        "Diaz",
        "Nunez",
    ],

    "Barcelona": [
        "Ter Stegen",
        "Kounde",
        "Araujo",
        "Cubarsi",
        "Balde",
        "Pedri",
        "De Jong",
        "Gavi",
        "Lamine Yamal",
        "Lewandowski",
        "Raphinha",
    ],

    "Bayern Munich": [
        "Neuer",
        "Kimmich",
        "Upamecano",
        "Kim Min-jae",
        "Davies",
        "Goretzka",
        "Musiala",
        "Olise",
        "Gnabry",
        "Kane",
        "Coman",
    ],
}


# ==================================================
# EVENT TYPES
# ==================================================

event_types = [
    "PASS",
    "SHOT",
    "SHOT_ON_TARGET",
    "GOAL",
    "FOUL",
    "TACKLE",
    "CORNER",
    "YELLOW_CARD",
    "RED_CARD",
    "SUBSTITUTION",
]


event_weights = [
    55,
    10,
    6,
    3,
    8,
    7,
    5,
    4,
    0.2,
    1,
]


# ==================================================
# CREATE MATCH
# ==================================================

def create_match(
    match_number,
    home_team,
    away_team
):

    return {

        "match_id":
            f"match_{match_number:03d}",

        "competition":
            "Friendly",

        "home_team":
            home_team,

        "away_team":
            away_team,

        "status":
            "LIVE",

        "current_minute":
            0,

        "created_at":
            datetime.now().isoformat(),
    }


# ==================================================
# CREATE EVENT
# ==================================================

def create_event(
    event_number,
    match,
    minute
):

    # ----------------------------------------------
    # Choose team
    # ----------------------------------------------

    team = random.choice([
        match["home_team"],
        match["away_team"],
    ])


    # ----------------------------------------------
    # Choose player
    # ----------------------------------------------

    player = random.choice(
        teams[team]
    )


    # ----------------------------------------------
    # Choose event
    # ----------------------------------------------

    event_type = random.choices(
        event_types,
        weights=event_weights,
        k=1
    )[0]


    # ----------------------------------------------
    # Pitch position
    # ----------------------------------------------

    x = round(
        random.uniform(0, 100),
        2
    )

    y = round(
        random.uniform(0, 100),
        2
    )


    # ----------------------------------------------
    # Expected goals
    # ----------------------------------------------

    if event_type in [
        "SHOT",
        "SHOT_ON_TARGET",
        "GOAL",
    ]:

        xg = round(
            random.uniform(
                0.02,
                0.85
            ),
            2
        )

    else:

        xg = 0.0


    # ==================================================
    # UNIQUE EVENT ID
    #
    # Example:
    #
    # match_003_evt_00001
    # match_003_evt_00002
    # match_004_evt_00003
    #
    # Because match_id changes every run,
    # old events will never conflict.
    # ==================================================

    event_id = (
        f"{match['match_id']}"
        f"_evt_{event_number:05d}"
    )


    # ==================================================
    # RETURN EVENT
    # ==================================================

    return {

        "event_id":
            event_id,

        "match_id":
            match["match_id"],

        "competition":
            match["competition"],

        "home_team":
            match["home_team"],

        "away_team":
            match["away_team"],

        "player":
            player,

        "team":
            team,

        "event_type":
            event_type,

        "minute":
            minute,

        "x":
            x,

        "y":
            y,

        "xg":
            xg,

        "timestamp":
            datetime.now().isoformat(),
    }


# ==================================================
# DIRECT TEST
# ==================================================

if __name__ == "__main__":

    match = create_match(
        1,
        "Chelsea",
        "Liverpool"
    )

    print(match)

    event = create_event(
        1,
        match,
        1
    )

    print(event)