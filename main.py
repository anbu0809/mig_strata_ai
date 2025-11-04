import uvicorn
import os
from backend.database import init_db

if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    # Run the FastAPI application
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )