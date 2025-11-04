from fastapi import APIRouter, BackgroundTasks
from backend.models import CommonResponse
import asyncio
import json
import os

router = APIRouter()

# Global variables to track migration status
structure_migration_status = {
    "phase": None,
    "percent": 0,
    "done": False,
    "error": None
}

data_migration_status = {
    "phase": None,
    "percent": 0,
    "done": False,
    "error": None
}

async def run_structure_migration_task():
    """Background task to run structure migration"""
    global structure_migration_status
    
    # Reset status
    structure_migration_status = {
        "phase": "Initializing",
        "percent": 0,
        "done": False,
        "error": None
    }
    
    # Simulate migration phases
    phases = [
        ("Loading extraction results", 10),
        ("Translating schema to target dialect", 30),
        ("Validating DDL syntax", 50),
        ("Creating tables in target", 70),
        ("Creating indexes and constraints", 90),
        ("Finalizing structure migration", 100)
    ]
    
    try:
        for phase, percent in phases:
            structure_migration_status["phase"] = phase
            structure_migration_status["percent"] = percent
            
            # Simulate work
            await asyncio.sleep(1)
        
        # Update status
        structure_migration_status["done"] = True
    except Exception as e:
        structure_migration_status["error"] = str(e)

async def run_data_migration_task():
    """Background task to run data migration"""
    global data_migration_status
    
    # Reset status
    data_migration_status = {
        "phase": "Initializing",
        "percent": 0,
        "done": False,
        "error": None
    }
    
    # Simulate migration phases
    phases = [
        ("Preparing data transfer", 10),
        ("Migrating users table (1500 rows)", 30),
        ("Migrating orders table (3500 rows)", 60),
        ("Migrating products table (800 rows)", 80),
        ("Validating data integrity", 90),
        ("Finalizing data migration", 100)
    ]
    
    try:
        for phase, percent in phases:
            data_migration_status["phase"] = phase
            data_migration_status["percent"] = percent
            
            # Simulate work
            await asyncio.sleep(1)
        
        # Update status
        data_migration_status["done"] = True
    except Exception as e:
        data_migration_status["error"] = str(e)

@router.post("/structure", response_model=CommonResponse)
async def migrate_structure(background_tasks: BackgroundTasks):
    global structure_migration_status
    structure_migration_status["phase"] = "Starting"
    structure_migration_status["percent"] = 0
    structure_migration_status["done"] = False
    
    background_tasks.add_task(run_structure_migration_task)
    
    return CommonResponse(ok=True, message="Structure migration started")

@router.post("/data", response_model=CommonResponse)
async def migrate_data(background_tasks: BackgroundTasks):
    global data_migration_status
    data_migration_status["phase"] = "Starting"
    data_migration_status["percent"] = 0
    data_migration_status["done"] = False
    
    background_tasks.add_task(run_data_migration_task)
    
    return CommonResponse(ok=True, message="Data migration started")

@router.get("/structure/status")
async def get_structure_migration_status():
    global structure_migration_status
    return structure_migration_status

@router.get("/data/status")
async def get_data_migration_status():
    global data_migration_status
    return data_migration_status