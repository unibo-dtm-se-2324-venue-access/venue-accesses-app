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

import json
import os
from fastapi import APIRouter, HTTPException, Query, Request, Depends, Form
from fastapi.responses import JSONResponse, StreamingResponse
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
    return JSONResponse(
            status_code=200,
            content={
                "message": "Presence logged successfully",
            }
        )


@api_router.post("/add_or_update_person")
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
        return JSONResponse(
            status_code=200,
            content={
                "message": "Person updated",
            }
        )
    else:
        service.add_person(rowId, first_name, last_name, email, role, hire_date, end_date, user_password)
        return  JSONResponse(
        status_code=200,
        content={
            "message": "Person added",
        }
    )

@api_router.post("/delete_person")
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

    return  JSONResponse(
        status_code=200,
        content={
            "message": "Person deleted",
        })


@api_router.get("/extract_delays", responses={200: {"content": {"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}}}}, response_class=StreamingResponse)
async def extract_delays(
    monthYear: date = Query(...),
    service: AccessService = Depends(AccessService),
):
    try:
        excel_file_path = service.extract_delays(monthYear)
        if not excel_file_path or not os.path.exists(excel_file_path):
            raise HTTPException(status_code=404, detail="Excel file not fund.")

        def iterfile():
            with open(excel_file_path, "rb") as file:
                yield from file
        
        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(excel_file_path)}"
        }

        return StreamingResponse(iterfile(), headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error extracting delays: {str(e)}")

@api_router.get("/create_excel_report")
async def create_excel_report(
    monthYear: date = Query(...),
    service: AccessService = Depends(AccessService),
):
    try:
        excel_file_path = service.create_excel_report(monthYear)
        if not excel_file_path or not os.path.exists(excel_file_path):
            raise HTTPException(status_code=404, detail="Excel file not fund.")

        def iterfile():
            with open(excel_file_path, "rb") as file:
                yield from file
        
        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(excel_file_path)}"
        }

        return StreamingResponse(iterfile(), headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"Error extracting delays: {str(e)}")