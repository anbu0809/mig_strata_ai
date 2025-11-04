from fastapi import APIRouter
from backend.models import SetSourceTargetRequest, SessionResponse
from backend.database import set_source_target, get_active_session

router = APIRouter()

@router.post("/set-source-target")
async def set_source_target_endpoint(request: SetSourceTargetRequest):
    set_source_target(request.sourceId, request.targetId)
    return {"ok": True}

@router.get("/", response_model=SessionResponse)
async def get_session():
    session = get_active_session()
    return SessionResponse(**session)