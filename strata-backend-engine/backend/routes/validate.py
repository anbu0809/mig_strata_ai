from fastapi import APIRouter, BackgroundTasks
from backend.models import CommonResponse
import asyncio
import json
import os
import random

router = APIRouter()

# Global variable to track validation status
validation_status = {
    "phase": None,
    "percent": 0,
    "done": False,
    "results": None
}

def generate_validation_results():
    """Generate mock validation results"""
    categories = [
        "Schema Validation",
        "Table Structure Match",
        "Constraints",
        "Views",
        "Triggers",
        "Indexes",
        "Stored Procedures",
        "Sequences",
        "Row Counts",
        "Data Checksums",
        "Sample Comparisons",
        "Null Ratios",
        "Referential Integrity",
        "Data Type Conversion",
        "Encoding Preservation",
        "Date/Timezone",
        "Users & Roles",
        "Privileges",
        "Ownership",
        "Schema Access",
        "Query Performance",
        "Index Efficiency",
        "Jobs/Schedulers",
        "Storage",
        "Version/Config"
    ]
    
    results = []
    for category in categories:
        status = random.choice(["Pass", "Fail"]) if random.random() > 0.2 else "Pass"
        results.append({
            "category": category,
            "status": status,
            "errorDetails": f"Error in {category}" if status == "Fail" else None,
            "suggestedFix": f"Suggested fix for {category}" if status == "Fail" else None,
            "confidenceScore": round(random.uniform(0.7, 1.0), 2) if status == "Fail" else 1.0
        })
    
    return results

async def run_validation_task():
    """Background task to run validation"""
    global validation_status
    
    # Reset status
    validation_status = {
        "phase": "Initializing",
        "percent": 0,
        "done": False,
        "results": None
    }
    
    # Simulate validation phases
    phases = [
        ("Loading migration results", 5),
        ("Running structural validations", 20),
        ("Checking data integrity", 40),
        ("Validating security settings", 60),
        ("Performance benchmarking", 80),
        ("Generating validation report", 100)
    ]
    
    for phase, percent in phases:
        validation_status["phase"] = phase
        validation_status["percent"] = percent
        
        # Simulate work
        await asyncio.sleep(1)
    
    # Generate validation results
    results = generate_validation_results()
    
    # Save to artifacts directory
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/validation_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Update status
    validation_status["done"] = True
    validation_status["results"] = results

@router.post("/run", response_model=CommonResponse)
async def run_validation(background_tasks: BackgroundTasks):
    global validation_status
    validation_status["phase"] = "Starting"
    validation_status["percent"] = 0
    validation_status["done"] = False
    
    background_tasks.add_task(run_validation_task)
    
    return CommonResponse(ok=True, message="Validation started")

@router.get("/status")
async def get_validation_status():
    global validation_status
    return validation_status

@router.get("/report")
async def get_validation_report():
    # Load validation report if exists
    if os.path.exists("artifacts/validation_report.json"):
        with open("artifacts/validation_report.json", "r") as f:
            return json.load(f)
    return []