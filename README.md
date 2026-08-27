# Real-Time Football Analytics Data Pipeline

A real-time data engineering portfolio project that simulates football match events and processes them through an end-to-end streaming architecture using **Apache Kafka, Apache Spark, PostgreSQL, FastAPI, and React**.

The project demonstrates how live event data can be generated, streamed, processed, stored, exposed through an API, and visualized in a frontend dashboard.

---

## Project Overview

This project simulates multiple live football matches and continuously generates events such as:

- Passes
- Shots
- Goals
- Fouls
- Tackles
- Yellow cards
- Red cards
- Substitutions
- Corners
- Expected Goals (xG)

Events are produced into Kafka in real time, processed using Spark Structured Streaming, stored in PostgreSQL, exposed through FastAPI, and displayed in a React dashboard.

The goal of the project is to demonstrate practical data engineering concepts including:

- Real-time event ingestion
- Kafka partitioning
- Stream processing
- Event-driven architecture
- Idempotent processing
- Aggregation of streaming data
- Database persistence
- API-based data serving
- End-to-end pipeline orchestration

---

## Architecture

```text
                  ┌──────────────────────┐
                  │  Football Simulator  │
                  │    Python Producer   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Apache Kafka     │
                  │  Real-Time Events    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     Apache Spark     │
                  │ Structured Streaming │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │      PostgreSQL      │
                  │ Events + Aggregates  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │       FastAPI        │
                  │     REST API Layer   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     React + Vite     │
                  │ Analytics Dashboard  │
                  └──────────────────────┘
```

---

## Data Pipeline

### 1. Event Generation

The Python event generator creates simulated football events for live matches.

Each event contains fields such as:

```json
{
  "event_id": "evt_00001",
  "match_id": "match_001",
  "player_id": "player_007",
  "team_id": "team_101",
  "event_type": "PASS",
  "minute": 23,
  "x": 64,
  "y": 41,
  "xg": 0.0,
  "timestamp": "2026-08-26T09:30:15"
}
```

The generator simulates the progress of a football match by producing events continuously.

---

### 2. Kafka Producer

The producer sends generated football events to Apache Kafka.

Kafka acts as the real-time event transport layer between the simulator and the stream-processing system.

The project also simulates multiple matches at the same time, allowing event streams to be processed independently.

Key Kafka concepts demonstrated:

- Producers
- Topics
- Partitions
- Event ordering
- Streaming ingestion
- Decoupled architecture

---

### 3. Spark Structured Streaming

Apache Spark consumes football events directly from Kafka.

Spark parses incoming JSON events and processes them in streaming micro-batches.

The streaming job:

- Reads Kafka events
- Parses the event schema
- Persists raw football events
- Identifies affected matches
- Calculates updated team statistics
- Writes aggregated statistics to PostgreSQL

Calculated metrics include:

- Shots
- Shots on target
- Passes
- Fouls
- Yellow cards
- Corners
- Expected Goals (xG)

---

## Idempotent Stream Processing

A key design consideration in this project is preventing duplicate statistics when Spark retries a micro-batch.

Instead of incrementing previously stored statistics with every Spark batch, the pipeline recalculates the latest totals from the persisted raw events.

Conceptually:

```text
Kafka Event
    ↓
Store Raw Event
    ↓
Query Current Match Events
    ↓
Recalculate Aggregates
    ↓
Update Team Statistics
```

This prevents repeated Spark batches from incorrectly increasing statistics multiple times.

The raw event table acts as the source of truth, while the team statistics table represents derived analytical data.

---

## Data Model

The pipeline logically separates raw and aggregated data.

### Raw Event Layer

Stores individual football events.

Example fields:

```text
event_id
match_id
team
player_id
event_type
minute
x
y
xg
timestamp
```

### Match Layer

Stores information about each simulated match.

Example fields:

```text
match_id
home_team
away_team
status
current_minute
started_at
ended_at
```

### Aggregated Statistics Layer

Stores continuously updated statistics for each team.

Example fields:

```text
match_id
team
shots
shots_on_target
passes
fouls
yellow_cards
corners
xg
updated_at
```

---

## API Layer

FastAPI provides a REST API for accessing processed football data.

Available routes include:

```text
GET /
GET /matches
GET /matches/{match_id}
GET /matches/{match_id}/team-stats
```

The API connects to PostgreSQL and returns match data, events, and calculated statistics to the frontend.

---

## Frontend Dashboard

The frontend is built using:

- React
- Vite
- React Router

Main pages include:

### Live Matches

Displays the latest simulated football matches with live score and statistics.

### Match Details

Displays detailed information for a selected match.

### Match History

Displays previously completed matches.

### Match Timeline

Displays recent football events in chronological order.

### Statistics

Displays team metrics such as:

- Shots
- Passes
- Fouls
- Cards
- xG

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Event simulation and pipeline scripts |
| Apache Kafka | Real-time event streaming |
| Apache Spark | Stream processing and aggregation |
| PostgreSQL | Persistent event and analytics storage |
| FastAPI | REST API and serving layer |
| React | Analytics dashboard |
| Vite | Frontend development/build tooling |
| Docker Compose | Local Kafka infrastructure |

---

## Repository Structure

```text
.
├── frontend/
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── components/
│       │   ├── MatchHeader.jsx
│       │   ├── Navbar.jsx
│       │   ├── StatsTable.jsx
│       │   └── Timeline.jsx
│       ├── pages/
│       │   ├── HistoryPage.jsx
│       │   ├── LiveMatchPage.jsx
│       │   └── MatchDetailsPage.jsx
│       ├── App.jsx
│       └── main.jsx
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── generator/
│   │   ├── event_generator.py
│   │   └── README.md
│   │
│   ├── producer/
│   │   ├── kafka_producer.py
│   │   └── kafka_producer_test.py
│   │
│   └── spark/
│       ├── kafka_read.py
│       └── spark_basics.py
│
├── docker-compose.yml
├── run_pipeline.py
└── README.md
```

---

## Running the Project

### Prerequisites

Install the following:

- Python 3
- Java
- Apache Spark
- PostgreSQL
- Docker
- Node.js
- npm

---

### 1. Start Kafka

```bash
docker compose up -d
```

Kafka is exposed on:

```text
localhost:9092
```

---

### 2. Start PostgreSQL

Make sure PostgreSQL is running and the required database and tables have been created.

Database connection details should ideally be configured using environment variables.

Example:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=football
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

---

### 3. Install Python Dependencies

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux / macOS
source .venv/bin/activate
```

```bash
# Windows
.venv\Scripts\activate
```

Install the required Python packages for Kafka, Spark, PostgreSQL, and FastAPI.

---

### 4. Start the Streaming Pipeline

Run the producer and Spark processing jobs.

Depending on the project setup, this can be started manually or through:

```bash
python run_pipeline.py
```

The producer generates football events while Spark consumes and processes them.

---

### 5. Start the FastAPI Server

Example:

```bash
uvicorn src.api.main:app --reload
```

The API will typically be available at:

```text
http://localhost:8000
```

---

### 6. Start the Frontend

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL shown by Vite in your browser.

---

## Data Engineering Concepts Demonstrated

This project was built specifically to demonstrate practical data engineering skills.

### Event-Driven Architecture

Services communicate through events rather than direct application-to-application calls.

### Real-Time Streaming

Football events are processed continuously rather than in a scheduled batch job.

### Kafka Partitioning

Multiple matches can be processed concurrently while preserving event ordering for an individual match.

### Stream Processing

Spark Structured Streaming consumes and transforms incoming Kafka data.

### Idempotency

Aggregated statistics are recalculated from persisted raw events to reduce the risk of duplicate Spark batch processing.

### Raw vs Derived Data

Raw football events are retained separately from analytical aggregates.

### Data Serving

Processed data is made available through FastAPI for downstream applications.

### End-to-End Pipeline Design

The project covers the complete lifecycle:

```text
Generation
→ Ingestion
→ Processing
→ Storage
→ API
→ Visualization
```

---

## Current Improvements / Roadmap

Planned improvements include:

- Add PostgreSQL to Docker Compose
- Add database initialization SQL scripts
- Introduce environment-based configuration
- Add Kafka message keys based on `match_id`
- Add stronger event-level uniqueness constraints
- Add Spark checkpoint configuration
- Add dead-letter handling for invalid events
- Add data validation
- Add structured logging
- Add automated tests
- Add monitoring and pipeline metrics
- Add Docker support for additional services
- Improve Kafka and Spark failure recovery
- Add more advanced football analytics

Possible future analytics:

- Possession percentage
- Pass completion rate
- Shot maps
- xG timelines
- Player-level statistics
- Match momentum
- Heatmaps
- League tables

---

## Why This Project?

Many beginner data engineering projects focus only on static CSV files and batch transformations.

This project was created to explore a more realistic streaming architecture where data is continuously generated and processed.

It demonstrates how several components of a modern data platform can work together:

```text
Kafka        → ingestion
Spark        → processing
PostgreSQL   → storage
FastAPI      → serving
React        → visualization
```

The project is intended as a portfolio demonstration of real-time data engineering fundamentals and distributed streaming concepts.

---

## Author

Built as a **Data Engineering Portfolio Project** focused on real-time event streaming, stream processing, and analytics pipeline design.
