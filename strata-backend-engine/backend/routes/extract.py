from fastapi import APIRouter, BackgroundTasks
from backend.models import CommonResponse, AnalysisStatusResponse
from backend.database import get_active_session
import asyncio
import json
import os

router = APIRouter()

# Global variable to track extraction status
extraction_status = {
    "phase": None,
    "percent": 0,
    "done": False,
    "results_summary": None
}

def create_extraction_bundle(analysis_bundle):
    """Create a mock extraction bundle based on analysis"""
    return {
        "ddl_scripts": {
            "tables": ["CREATE TABLE users (...)", "CREATE TABLE orders (...)"],
            "views": ["CREATE VIEW user_summary AS ..."],
            "indexes": ["CREATE INDEX idx_user_email ON users(email)"]
        },
        "constraints": ["PRIMARY KEY", "FOREIGN KEY", "UNIQUE"],
        "dependencies": ["users", "orders", "products"],
        "type_mappings": {"VARCHAR2": "VARCHAR", "NUMBER": "DECIMAL"},
        "security": ["GRANT SELECT ON users TO user_role"],
        "extraction_report": {
            "objects_extracted": 15,
            "warnings": 0
        }
    }

async def run_extraction_task():
    """Background task to run the extraction"""
    global extraction_status
    
    # Reset status
    extraction_status = {
        "phase": "Initializing",
        "percent": 0,
        "done": False,
        "results_summary": None
    }
    
    # Simulate extraction phases
    phases = [
        ("Loading analysis results", 10),
        ("Generating DDL scripts", 30),
        ("Extracting constraints", 50),
        ("Building dependency graph", 70),
        ("Preparing type mappings", 85),
        ("Finalizing extraction", 100)
    ]
    
    for phase, percent in phases:
        extraction_status["phase"] = phase
        extraction_status["percent"] = percent
        
        # Simulate work
        await asyncio.sleep(1)
    
    # Load analysis bundle if exists
    analysis_bundle = {}
    if os.path.exists("artifacts/analysis_bundle.json"):
        with open("artifacts/analysis_bundle.json", "r") as f:
            analysis_bundle = json.load(f)
    
    # Create extraction bundle
    extraction_bundle = create_extraction_bundle(analysis_bundle)
    
    # Save to artifacts directory
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/extraction_bundle.json", "w") as f:
        json.dump(extraction_bundle, f, indent=2)
    
    # Update status
    extraction_status["done"] = True
    extraction_status["results_summary"] = {
        "objects_extracted": extraction_bundle["extraction_report"]["objects_extracted"],
        "warnings": extraction_bundle["extraction_report"]["warnings"]
    }

@router.post("/start", response_model=CommonResponse)
async def start_extraction(background_tasks: BackgroundTasks):
    global extraction_status
    extraction_status["phase"] = "Starting"
    extraction_status["percent"] = 0
    extraction_status["done"] = False
    
    background_tasks.add_task(run_extraction_task)
    
    return CommonResponse(ok=True, message="Extraction started")

@router.get("/status", response_model=AnalysisStatusResponse)
async def get_extraction_status():
    global extraction_status
    return AnalysisStatusResponse(
        ok=True,
        phase=extraction_status["phase"],
        percent=extraction_status["percent"],
        done=extraction_status["done"],
        resultsSummary=extraction_status["results_summary"]
    )