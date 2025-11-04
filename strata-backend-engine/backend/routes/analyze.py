from fastapi import APIRouter, BackgroundTasks
from backend.models import AnalysisStatusResponse, CommonResponse
from backend.database import get_active_session
import asyncio
import json
import os

router = APIRouter()

# Global variable to track analysis status (in production, use Redis or database)
analysis_status = {
    "phase": None,
    "percent": 0,
    "done": False,
    "results_summary": None
}

def create_analysis_bundle(source_db_info):
    """Create a mock analysis bundle"""
    return {
        "database_type": source_db_info["dbType"] if source_db_info else "Unknown",
        "version": "1.0.0",
        "schemas": ["public", "sales", "hr"],
        "tables": [
            {"name": "users", "rows": 1500},
            {"name": "orders", "rows": 3500},
            {"name": "products", "rows": 800}
        ],
        "views": ["user_summary", "order_details"],
        "procedures": ["calculate_tax", "generate_report"],
        "indexes": ["idx_user_email", "idx_order_date"],
        "relationships": ["users->orders", "orders->products"],
        "data_types": ["VARCHAR", "INTEGER", "TIMESTAMP", "DECIMAL"],
        "security": ["admin_role", "user_role"],
        "environment": {"os": "Linux", "version": "1.0.0"},
        "profiling": {"users": {"null_ratio": 0.05}, "orders": {"null_ratio": 0.02}}
    }

async def run_analysis_task():
    """Background task to run the analysis"""
    global analysis_status
    
    # Reset status
    analysis_status = {
        "phase": "Initializing",
        "percent": 0,
        "done": False,
        "results_summary": None
    }
    
    # Simulate analysis phases
    phases = [
        ("Connecting to source database", 10),
        ("Analyzing database schema", 25),
        ("Extracting table structures", 40),
        ("Analyzing views and procedures", 55),
        ("Checking indexes and performance", 70),
        ("Profiling data samples", 85),
        ("Generating analysis report", 100)
    ]
    
    for phase, percent in phases:
        analysis_status["phase"] = phase
        analysis_status["percent"] = percent
        
        # Simulate work
        await asyncio.sleep(1)
    
    # Get session info
    session = get_active_session()
    source_db = session.get("source")
    
    # Create analysis bundle
    analysis_bundle = create_analysis_bundle(source_db)
    
    # Save to artifacts directory
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/analysis_bundle.json", "w") as f:
        json.dump(analysis_bundle, f, indent=2)
    
    # Update status
    analysis_status["done"] = True
    analysis_status["results_summary"] = {
        "tables_analyzed": len(analysis_bundle["tables"]),
        "views_found": len(analysis_bundle["views"]),
        "procedures_found": len(analysis_bundle["procedures"])
    }

@router.post("/start", response_model=CommonResponse)
async def start_analysis(background_tasks: BackgroundTasks):
    global analysis_status
    analysis_status["phase"] = "Starting"
    analysis_status["percent"] = 0
    analysis_status["done"] = False
    
    background_tasks.add_task(run_analysis_task)
    
    return CommonResponse(ok=True, message="Analysis started")

@router.get("/status", response_model=AnalysisStatusResponse)
async def get_analysis_status():
    global analysis_status
    return AnalysisStatusResponse(
        ok=True,
        phase=analysis_status["phase"],
        percent=analysis_status["percent"],
        done=analysis_status["done"],
        resultsSummary=analysis_status["results_summary"]
    )