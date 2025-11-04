#!/bin/bash

# Setup environment if needed
if [ ! -d "venv" ] || [ ! -d "frontend/node_modules" ]; then
    echo "Setting up development environment..."
    python dev_utils.py setup
fi

# Start both backend and frontend
echo "Starting Strata application..."
python dev_utils.py start-all

echo "Strata application started!"
echo "Frontend available at: http://localhost:3000"
echo "Backend available at: http://localhost:8000"