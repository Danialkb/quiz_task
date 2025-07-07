#!/bin/bash

echo "Running Alembic migrations..."
uv run alembic -c resources/migrations/alembic.ini upgrade head

echo "Populating Database"
uv run python -m commands.populate_db

echo "Starting the app..."
exec uv run uvicorn main:app --host 0.0.0.0 --port 8000
