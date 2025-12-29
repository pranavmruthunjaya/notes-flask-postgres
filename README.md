# Notes API with Flask + PostgreSQL

A minimal REST API built from scratch to demonstrate clean Python–SQL integration using Flask and PostgreSQL (Dockerized). The project focuses on fundamentals: schema design, safe SQL queries, and clear backend structure.

---

## Tech Stack

- Python 3  
- Flask  
- PostgreSQL (Docker)  
- psycopg  
- Docker Compose  

---

## What This Shows

- End-to-end API development with Flask  
- PostgreSQL schema design with indexes  
- Parameterized SQL queries (no ORM)  
- Transaction-safe database access  
- Clean, incremental project structure  
- Local development using Dockerized infrastructure  

---

## Current Features

- Health and database connectivity checks  
- Create notes (title, content)  
- List notes (latest first)  
- Persistent PostgreSQL storage via Docker volumes  

---

## Project Structure
notes-lite/
infra/
docker-compose.yml
backend/
app.py
db.py
schema.sql
requirements.txt


---

## Running Locally

Start PostgreSQL:
```bash
docker compose -f infra/docker-compose.yml up -d


Run backend:

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py


Create database schema:

docker exec -i notes_postgres psql -U notes_user -d notes_db < backend/schema.sql

API Overview

GET /health

GET /db-health

POST /api/notes

GET /api/notes

