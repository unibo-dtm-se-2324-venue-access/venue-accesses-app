import json
from fastapi import APIRouter, HTTPException, Query, Request, Depends, Form
from ..services.AccessService import AccessService
from ..db.db import DbManager, MySQLDb
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import qrcode
from datetime import date


api_router = APIRouter(prefix="/api", tags=["api"])

templates = Jinja2Templates(directory="app/templates")

@api_router.post("/insert_presence")
async def insert_presence(
    request: Request,
    id: str = Form(...),
    service: AccessService = Depends(AccessService),
):
    return service.insert_access(int(id))

@api_router.get("/extract_delays")
async def extract_delays(
    date: date = Query(..., description="The date to extract delays for"),
    service: AccessService = Depends(AccessService),
):
    try:
        delays = service.extract_delays(date)
        return delays
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error extracting delays: {str(e)}")