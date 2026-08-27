import subprocess
import sys
import time


processes = []


def start_process(command, name):
    print(f"Starting {name}...")

    process = subprocess.Popen(
        command,
        shell=True
    )

    processes.append(
        (name, process)
    )

    return process


try:

    print("=" * 60)
    print("       REAL-TIME FOOTBALL ANALYTICS PIPELINE")
    print("=" * 60)

    # -------------------------------------------------
    # 1. FASTAPI
    # -------------------------------------------------

    start_process(
        f"{sys.executable} -m uvicorn "
        "src.api.main:app "
        "--reload "
        "--port 8000",
        "FastAPI"
    )


    # -------------------------------------------------
    # 2. SPARK KAFKA READER
    # -------------------------------------------------

    start_process(
        f"{sys.executable} -m src.spark.kafka_read",
        "Spark Kafka Reader"
    )


    # Give Spark a moment to initialize before producer
    time.sleep(3)


    # -------------------------------------------------
    # 3. KAFKA PRODUCER
    # -------------------------------------------------

    start_process(
        f"{sys.executable} -m src.producer.kafka_producer",
        "Kafka Producer"
    )


    print()
    print("=" * 60)
    print("All services started.")
    print("=" * 60)
    print()
    print("FastAPI:")
    print("  http://localhost:8000")
    print()
    print("Press Ctrl+C to stop everything.")
    print()


    # -------------------------------------------------
    # KEEP MAIN SCRIPT RUNNING
    # -------------------------------------------------

    while True:

        time.sleep(1)


except KeyboardInterrupt:

    print()
    print("Stopping pipeline...")


finally:

    for name, process in processes:

        if process.poll() is None:

            print(
                f"Stopping {name}..."
            )

            process.terminate()


    for name, process in processes:

        try:

            process.wait(
                timeout=5
            )

        except subprocess.TimeoutExpired:

            print(
                f"Force stopping {name}..."
            )

            process.kill()


    print()
    print("Pipeline stopped.")