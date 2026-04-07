#!/bin/bash

# Create database tables if they don't exist
python -c "from app.database import init_db; init_db()"

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
