"""
 MIT License
 
 Copyright (c) 2024 Riccardo Leonelli
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 
"""

from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Query, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.dependencies import TokenData, get_current_employee, get_current_manager
from app.utility.DateUtility import DateUtility
from ..services.AccessService import AccessService
import json

view_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@view_router.get("/presence", response_class=HTMLResponse, include_in_schema=False)
async def get_registry_list(request: Request, 
                          date: str = Query(None),
                          service: AccessService = Depends(AccessService),
                          current_user: TokenData = Depends(get_current_manager)):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    result = service.get_access_by_date(date)
    for item in result:
        item['enter_time'] = DateUtility.format_time(item['enter_time'])
        item['exit_time'] = DateUtility.format_time(item['exit_time'])

    
    return templates.TemplateResponse(
        "presence.html",
        {
            "request": request, 
            "data": json.dumps(result, default=str),
            "selected_date": date 
        },
    )

@view_router.get("/personal_presence", response_class=HTMLResponse, include_in_schema=False)
async def get_registry_list(request: Request, 
                            date: str = Query(default=None, description="The date to filter access records, formatted as YYYY-MM-DD"),
                            service: AccessService = Depends(AccessService),
                            current_user: TokenData = Depends(get_current_employee)):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    try:
        result = service.get_access_by_employee(date, current_user)
        for item in result:
            item['access_date'] = DateUtility.format_date(item['access_date'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return templates.TemplateResponse(
        "personal_page.html",
        {
            "request": request, 
            "data": json.dumps(result, default=str),
            "selected_date": date 
        },
    )


@view_router.get("/scanQR", response_class=HTMLResponse, include_in_schema=False)
async def read_home(request: Request, current_user: TokenData = Depends(get_current_manager)):
    return templates.TemplateResponse(
        "qr_scan_page.html", {"request": request, "title": "Scan QR"}
    )


@view_router.get("/registry", response_class=HTMLResponse, include_in_schema=False)
async def get_registry_list(
    request: Request, service: AccessService = Depends(AccessService)
):
    result = service.get_registry()
    return templates.TemplateResponse(
        "people_page.html",
        {"request": request, "data": json.dumps(result, default=str)},
    )


@view_router.post("/add_or_update_person", include_in_schema=False)
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

@view_router.post("/delete_person", include_in_schema=False)
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


@view_router.post("/insert_presence", include_in_schema=False)
async def insert_presence(
    request: Request,
    personId: int = Form(...),
    timestamp: str = Form(...),
    service: AccessService = Depends(AccessService),
    current_user: TokenData = Depends(get_current_manager)
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

