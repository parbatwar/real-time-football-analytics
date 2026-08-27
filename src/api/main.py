from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2


app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="football_db",
        user="postgres",
        password="postgres"
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Football Analytics API is running"
    }


# ============================================================
# GET ALL MATCHES
# ============================================================

@app.get("/matches")
def get_matches():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            match_id,
            competition,
            home_team,
            away_team,
            status,
            current_minute
        FROM matches
        ORDER BY match_id;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    matches = []

    for row in rows:

        matches.append({
            "match_id": row[0],
            "competition": row[1],
            "home_team": row[2],
            "away_team": row[3],
            "status": row[4],
            "current_minute": row[5]
        })

    return matches


# ============================================================
# GET ONE MATCH
# ============================================================

@app.get("/matches/{match_id}")
def get_match(match_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            match_id,
            competition,
            home_team,
            away_team,
            status,
            current_minute
        FROM matches
        WHERE match_id = %s;
        """,
        (
            match_id,
        )
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:

        return {
            "message": "Match not found"
        }

    return {
        "match_id": row[0],
        "competition": row[1],
        "home_team": row[2],
        "away_team": row[3],
        "status": row[4],
        "current_minute": row[5]
    }


# ============================================================
# TEAM STATS FOR ONE MATCH
# ============================================================

@app.get("/matches/{match_id}/team-stats")
def get_team_stats(match_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            team,
            possession,
            shots,
            shots_on_target,
            passes,
            pass_accuracy,
            corners,
            fouls,
            yellow_cards,
            xg
        FROM team_match_stats
        WHERE match_id = %s
        ORDER BY team;
        """,
        (
            match_id,
        )
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    stats = []

    for row in rows:

        stats.append({
            "team": row[0],
            "possession": row[1],
            "shots": row[2],
            "shots_on_target": row[3],
            "passes": row[4],
            "pass_accuracy": row[5],
            "corners": row[6],
            "fouls": row[7],
            "yellow_cards": row[8],
            "xg": float(row[9] or 0)
        })

    return stats


# ============================================================
# EVENTS FOR ONE MATCH
# ============================================================

@app.get("/matches/{match_id}/events")
def get_events(
    match_id: str
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            event_id,
            minute,
            team,
            player,
            event_type,
            xg
        FROM match_events
        WHERE match_id = %s
        ORDER BY minute DESC, event_id DESC;
        """,
        (
            match_id,
        )
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    events = []

    for row in rows:

        events.append({
            "event_id": row[0],
            "minute": row[1],
            "team": row[2],
            "player": row[3],
            "event_type": row[4],
            "xg": float(row[5] or 0)
        })

    return events