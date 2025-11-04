#!/bin/bash

echo "Starting Strata Backend Engine..."
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Initialize database if needed
if [ ! -f "strata.db" ]; then
    echo "Initializing database..."
    python init_db.py
fi

# Start the server
echo "Starting server..."
echo "The API will be available at http://localhost:8000"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload