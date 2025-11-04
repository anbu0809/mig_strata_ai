from fastapi import APIRouter
from backend.models import CommonResponse
from backend.database import reset_session
import shutil
import os

router = APIRouter()

@router.post("/reset", response_model=CommonResponse)
async def reset_application():
    try:
        # Reset active session
        reset_session()
        
        # Clear artifacts directory
        if os.path.exists("artifacts"):
            shutil.rmtree("artifacts")
        
        return CommonResponse(ok=True, message="Application reset successfully")
    except Exception as e:
        return CommonResponse(ok=False, message=str(e))