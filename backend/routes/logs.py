from fastapi import APIRouter, HTTPException, Query
from backend.database import fetch_logs, fetch_user_logs

router = APIRouter()

@router.get("/logs/all")
def logs_all(limit: int = Query(100)):
    try:
        return fetch_logs(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs/user")
def logs_user(email: str):
    try:
        return fetch_user_logs(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
