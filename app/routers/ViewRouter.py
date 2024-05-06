from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Query, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.dependencies import TokenData, get_current_user

from ..services.AccessService import AccessService
import json

view_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def format_time(access_time):
    try:
        return access_time.strftime('%H:%M')
    except ValueError:
        return access_time 


@view_router.get("/presence", response_class=HTMLResponse)
async def get_registry_list(request: Request, 
                          date: str = Query(None),
                          service: AccessService = Depends(AccessService),
                          current_user: TokenData = Depends(get_current_user)):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    result = service.get_access_by_date(date)
    for item in result:
        item['access_time'] = format_time(item['access_time'])

    
    return templates.TemplateResponse(
        "presence.html",
        {
            "request": request, 
            "data": json.dumps(result, default=str),
            "selected_date": date 
        },
    )


@view_router.get("/scanQR", response_class=HTMLResponse)
async def read_home(request: Request, current_user: TokenData = Depends(get_current_user)):
    return templates.TemplateResponse(
        "qr_scan_page.html", {"request": request, "title": "Scan QR"}
    )


@view_router.get("/registry", response_class=HTMLResponse)
async def get_registry_list(
    request: Request, service: AccessService = Depends(AccessService)
):
    result = service.get_registry()
    return templates.TemplateResponse(
        "people_page.html",
        {"request": request, "data": json.dumps(result, default=str)},
    )


@view_router.post("/add_or_update_person")
async def add_or_update_person(
    request: Request,
    rowId: int = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    role: str = Form(...),
    hire_date: str = Form(None),
    end_date: str = Form(None),
    user_password: str = Form(None),
    service: AccessService = Depends(AccessService),
):
    
    if service.person_exists(rowId):
        service.update_person(rowId, first_name, last_name, email, role, hire_date, end_date, user_password)
    else:
        service.add_person(rowId, first_name, last_name, email, role, hire_date, end_date, user_password)
    
    return templates.TemplateResponse(
        "people_page.html",
        {"request": request, "data": json.dumps(service.get_registry(), default=str)},
    )

@view_router.post("/delete_person")
async def delete_person(
    request: Request,     
    rowId: int = Form(...), 
    service: AccessService = Depends(AccessService),
):
    if service.person_exists(rowId):
        service.delete_person(rowId)
        message = "Person deleted successfully"
    else:
        message = "Person not found"

    return templates.TemplateResponse(
        "people_page.html",
        {"request": request, message: message,  "data": json.dumps(service.get_registry(), default=str)},
    )


@view_router.post("/insert_presence")
async def insert_presence(
    request: Request,
    personId: int = Form(...),
    timestamp: str = Form(...),
    service: AccessService = Depends(AccessService),
    current_user: TokenData = Depends(get_current_user)
):
    if service.person_exists(personId):
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")

        service.insert_access_manual(personId, timestamp,current_user.username)
        message = "access insert correctly"
    else:
        message = "Person not found"

    return templates.TemplateResponse(
        "people_page.html",
        {"request": request, "message": message, "data": json.dumps(service.get_registry(), default=str)},
    )

