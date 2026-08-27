from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count


spark = SparkSession.builder \
    .appName("FootballAnalytics") \
    .master("local[*]") \
    .getOrCreate()


data = [
    ("match_001", "team01", "PASS"),
    ("match_001", "team01", "PASS"),
    ("match_001", "team01", "SHOT"),
    ("match_001", "team01", "GOAL"),
    ("match_001", "team02", "PASS"),
    ("match_001", "team02", "SHOT"),
    ("match_001", "team02", "PASS"),
    ("match_001", "team02", "GOAL"),
    ("match_001", "team02", "FOUL"),
]


df = spark.createDataFrame(
    data,
    ["match_id", "team_id", "event_type"]
)


team_stats = df.groupBy(
    "team_id"
).agg(
    count("*").alias("total_events")
)

team_stats.show()


spark.stop()