from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    from_json,
    col,
    sum,
    when
)

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType
)

import psycopg2


# ============================================================
# SPARK SESSION
# ============================================================

spark = (
    SparkSession.builder

    .appName(
        "FootballKafkaStreaming"
    )

    .master(
        "local[*]"
    )

    .config(
        "spark.jars.packages",

        "org.apache.spark:"
        "spark-sql-kafka-0-10_2.13:"
        "4.2.0,"

        "org.postgresql:"
        "postgresql:"
        "42.7.7"
    )

    .getOrCreate()
)


spark.sparkContext.setLogLevel(
    "WARN"
)


# ============================================================
# FOOTBALL EVENT SCHEMA
# ============================================================

event_schema = StructType([

    StructField(
        "event_id",
        StringType(),
        True
    ),

    StructField(
        "match_id",
        StringType(),
        True
    ),

    StructField(
        "competition",
        StringType(),
        True
    ),

    StructField(
        "home_team",
        StringType(),
        True
    ),

    StructField(
        "away_team",
        StringType(),
        True
    ),

    StructField(
        "player",
        StringType(),
        True
    ),

    StructField(
        "team",
        StringType(),
        True
    ),

    StructField(
        "event_type",
        StringType(),
        True
    ),

    StructField(
        "minute",
        IntegerType(),
        True
    ),

    StructField(
        "x",
        DoubleType(),
        True
    ),

    StructField(
        "y",
        DoubleType(),
        True
    ),

    StructField(
        "xg",
        DoubleType(),
        True
    ),

    StructField(
        "timestamp",
        StringType(),
        True
    ),
])


# ============================================================
# READ FROM KAFKA
# ============================================================

kafka_df = (

    spark
    .readStream

    .format(
        "kafka"
    )

    .option(
        "kafka.bootstrap.servers",
        "localhost:9092"
    )

    .option(
        "subscribe",
        "football-events"
    )

    .option(
        "startingOffsets",
        "latest"
    )

    .option(
        "failOnDataLoss",
        "false"
    )

    .load()
)


# ============================================================
# KAFKA VALUE → STRING
# ============================================================

events = kafka_df.select(

    col(
        "value"
    )

    .cast(
        "string"
    )

    .alias(
        "json_value"
    )
)


# ============================================================
# PARSE JSON
# ============================================================

parsed_events = (

    events

    .select(

        from_json(

            col(
                "json_value"
            ),

            event_schema

        ).alias(
            "event"
        )
    )

    .select(
        "event.*"
    )
)


# ============================================================
# WRITE BATCH TO POSTGRESQL
# ============================================================

def write_to_postgres(
    batch_df,
    batch_id
):

    # --------------------------------------------------------
    # Ignore empty batches
    # --------------------------------------------------------

    if batch_df.isEmpty():

        return


    print()
    print("=" * 70)

    print(
        f"                    WRITING BATCH {batch_id}"
    )

    print("=" * 70)


    # ========================================================
    # DEBUG
    # ========================================================

    print(
        "\nMATCHES RECEIVED BY SPARK:"
    )

    (
        batch_df
        .select(
            "match_id"
        )
        .distinct()
        .show(
            truncate=False
        )
    )


    print(
        "\nEVENT COUNT BY MATCH:"
    )

    (
        batch_df
        .groupBy(
            "match_id"
        )
        .count()
        .show(
            truncate=False
        )
    )


    print(
        "\nEVENTS RECEIVED:"
    )

    batch_df.show(
        20,
        truncate=False
    )


    # ========================================================
    # POSTGRES CONNECTION
    # ========================================================

    conn = psycopg2.connect(

        host="localhost",

        port=5433,

        database="football_db",

        user="postgres",

        password="postgres"
    )


    cursor = (
        conn.cursor()
    )


    try:

        # ====================================================
        # 1. INSERT / UPDATE MATCHES FIRST
        # ====================================================

        print(
            "\nWriting matches first..."
        )


        match_rows = (

            batch_df

            .select(

                "match_id",

                "competition",

                "home_team",

                "away_team"
            )

            .filter(
                col("match_id").isNotNull()
            )

            .distinct()

            .collect()
        )


        for match in match_rows:

            match_id = (
                match["match_id"]
            )

            # ----------------------------------------------
            # Find current minute
            # ----------------------------------------------

            current_minute_row = (

                batch_df

                .filter(
                    col("match_id")
                    == match_id
                )

                .selectExpr(
                    "MAX(minute) "
                    "AS max_minute"
                )

                .collect()[0]
            )


            current_minute = (
                current_minute_row[
                    "max_minute"
                ]
            )


            if current_minute is None:

                current_minute = 0


            # ----------------------------------------------
            # Insert/update match
            # ----------------------------------------------

            cursor.execute(
                """
                INSERT INTO matches
                (
                    match_id,
                    competition,
                    home_team,
                    away_team,
                    status,
                    current_minute
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

                ON CONFLICT (match_id)

                DO UPDATE SET

                    competition =
                        EXCLUDED.competition,

                    home_team =
                        EXCLUDED.home_team,

                    away_team =
                        EXCLUDED.away_team,

                    status =
                        EXCLUDED.status,

                    current_minute =
                        GREATEST(
                            matches.current_minute,
                            EXCLUDED.current_minute
                        )
                """,

                (
                    match["match_id"],

                    match["competition"],

                    match["home_team"],

                    match["away_team"],

                    "LIVE",

                    current_minute
                )
            )


            print(
                f"Match {match_id} "
                f"inserted/updated: "
                f"{match['home_team']} "
                f"vs "
                f"{match['away_team']} "
                f"({current_minute}')"
            )


        # ====================================================
        # 2. INSERT RAW EVENTS
        # ====================================================

        print(
            "\nWriting match events..."
        )


        event_rows = (

            batch_df

            .select(

                "event_id",

                "match_id",

                "minute",

                "team",

                "player",

                "event_type",

                "x",

                "y",

                "xg"
            )

            .filter(
                col("event_id")
                .isNotNull()
            )

            .collect()
        )


        inserted_events = 0


        for row in event_rows:

            cursor.execute(
                """
                INSERT INTO match_events
                (
                    event_id,
                    match_id,
                    minute,
                    team,
                    player,
                    event_type,
                    x,
                    y,
                    xg
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )

                ON CONFLICT (event_id)

                DO NOTHING
                """,

                (
                    row["event_id"],

                    row["match_id"],

                    row["minute"],

                    row["team"],

                    row["player"],

                    row["event_type"],

                    row["x"],

                    row["y"],

                    row["xg"]
                )
            )


            if cursor.rowcount > 0:

                inserted_events += 1


        print(
            f"Received {len(event_rows)} events."
        )

        print(
            f"Inserted {inserted_events} new events."
        )


        # ====================================================
        # 3. CALCULATE STATS FROM POSTGRES EVENTS
        #
        # Instead of adding the same Spark batch repeatedly,
        # calculate the full current totals from match_events.
        # This prevents doubled stats when Spark retries.
        # ====================================================

        print(
            "\nCalculating team statistics..."
        )


        affected_match_ids = [

            row["match_id"]

            for row in match_rows
        ]


        for match_id in affected_match_ids:

            # ----------------------------------------------
            # Find teams
            # ----------------------------------------------

            cursor.execute(
                """
                SELECT DISTINCT team

                FROM match_events

                WHERE match_id = %s

                AND team IS NOT NULL
                """,

                (
                    match_id,
                )
            )


            db_teams = [

                row[0]

                for row in (
                    cursor.fetchall()
                )
            ]


            for team in db_teams:

                # ------------------------------------------
                # Calculate full totals
                # ------------------------------------------

                cursor.execute(
                    """
                    SELECT

                        COUNT(*)
                        FILTER (
                            WHERE event_type = 'SHOT'
                        )
                        AS shots,

                        COUNT(*)
                        FILTER (
                            WHERE event_type =
                            'SHOT_ON_TARGET'
                        )
                        AS shots_on_target,

                        COUNT(*)
                        FILTER (
                            WHERE event_type = 'PASS'
                        )
                        AS passes,

                        COUNT(*)
                        FILTER (
                            WHERE event_type = 'FOUL'
                        )
                        AS fouls,

                        COUNT(*)
                        FILTER (
                            WHERE event_type =
                            'YELLOW_CARD'
                        )
                        AS yellow_cards,

                        COUNT(*)
                        FILTER (
                            WHERE event_type = 'CORNER'
                        )
                        AS corners,

                        COUNT(*)
                        FILTER (
                            WHERE event_type = 'GOAL'
                        )
                        AS goals,

                        COALESCE(
                            SUM(xg),
                            0
                        )
                        AS xg

                    FROM match_events

                    WHERE match_id = %s

                    AND team = %s
                    """,

                    (
                        match_id,
                        team
                    )
                )


                stats = (
                    cursor.fetchone()
                )


                shots = stats[0]
                shots_on_target = stats[1]
                passes = stats[2]
                fouls = stats[3]
                yellow_cards = stats[4]
                corners = stats[5]
                goals = stats[6]
                xg = stats[7]


                print(
                    f"{match_id} | "
                    f"{team} | "
                    f"Shots: {shots} | "
                    f"SOT: {shots_on_target} | "
                    f"Passes: {passes} | "
                    f"Goals: {goals} | "
                    f"xG: {xg}"
                )


                # ==========================================
                # 4. UPSERT TEAM STATISTICS
                # ==========================================

                cursor.execute(
                    """
                    INSERT INTO team_match_stats
                    (
                        match_id,
                        team,
                        shots,
                        shots_on_target,
                        passes,
                        fouls,
                        yellow_cards,
                        corners,
                        xg
                    )

                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )

                    ON CONFLICT (
                        match_id,
                        team
                    )

                    DO UPDATE SET

                        shots =
                            EXCLUDED.shots,

                        shots_on_target =
                            EXCLUDED.shots_on_target,

                        passes =
                            EXCLUDED.passes,

                        fouls =
                            EXCLUDED.fouls,

                        yellow_cards =
                            EXCLUDED.yellow_cards,

                        corners =
                            EXCLUDED.corners,

                        xg =
                            EXCLUDED.xg,

                        updated_at =
                            CURRENT_TIMESTAMP
                    """,

                    (
                        match_id,

                        team,

                        shots,

                        shots_on_target,

                        passes,

                        fouls,

                        yellow_cards,

                        corners,

                        xg
                    )
                )


        # ====================================================
        # 5. COMMIT
        # ====================================================

        conn.commit()


        print()
        print("=" * 70)

        print(
            "                  BATCH WRITTEN SUCCESSFULLY"
        )

        print("=" * 70)


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        conn.rollback()

        print()
        print("=" * 70)
        print(
            "                         ERROR"
        )
        print("=" * 70)

        print(
            e
        )

        raise


    finally:

        cursor.close()

        conn.close()


# ============================================================
# START STREAM
# ============================================================

query = (

    parsed_events

    .writeStream

    .foreachBatch(
        write_to_postgres
    )

    .outputMode(
        "append"
    )

    .option(
        "checkpointLocation",
        "checkpoints/postgres_write"
    )

    .trigger(
        processingTime="2 seconds"
    )

    .start()
)


# ============================================================
# START MESSAGE
# ============================================================

print()
print("=" * 70)

print(
    "                 SPARK KAFKA STREAMING"
)

print("=" * 70)

print()

print(
    "Listening to Kafka topic:"
)

print(
    "  → football-events"
)

print()

print(
    "Writing to PostgreSQL:"
)

print(
    "  → matches"
)

print(
    "  → match_events"
)

print(
    "  → team_match_stats"
)

print()

print("=" * 70)


# ============================================================
# KEEP APPLICATION RUNNING
# ============================================================

query.awaitTermination()