@echo off
echo Starting Strata Backend Engine...
echo =================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Initialize database if needed
if not exist "strata.db" (
    echo Initializing database...
    python init_db.py
)

REM Start the server
echo Starting server...
echo The API will be available at http://localhost:8000
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload