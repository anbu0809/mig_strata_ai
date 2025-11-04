@echo off

REM Setup environment if needed
if not exist "venv" (
    echo Setting up development environment...
    python dev_utils.py setup
)

if not exist "frontend\node_modules" (
    echo Setting up development environment...
    python dev_utils.py setup
)

REM Start both backend and frontend
echo Starting Strata application...
python dev_utils.py start-all

echo Strata application started!
echo Frontend available at: http://localhost:3000
echo Backend available at: http://localhost:8000
pause