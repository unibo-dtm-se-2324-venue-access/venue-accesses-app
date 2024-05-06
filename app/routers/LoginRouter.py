from datetime import timedelta, datetime
from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, Response
from app.model.PersonModel import PersonModel
from app.entities.Person import Person
from app.dependencies import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
  prefix="/token",
  tags=["login"]
)

@router.post("/")
def get_auth_token(response: Response, request: Request, background_task: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends(), language: str | None = Header(default='it')):
    user_model = PersonModel()
    user: Person = user_model.get_user_info_auth(form_data.username)
    
    if not user:
        return JSONResponse(
            status_code=401,
            content="user_not_found",
            headers={"WWW-Authenticate": "Bearer"},
        )        
    elif not user_model.check_password(stored_password=user.user_password, password=form_data.password):
        return JSONResponse(
            status_code=401,
            content="username_password_error",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=480)
    access_token = create_access_token(user.__dict__, expires_delta=access_token_expires)

    response.set_cookie(key="access_token", value=access_token, expires=int(access_token_expires.total_seconds()))


    return JSONResponse(
        status_code=200,
        content={
            "message": "Login successful",
            "userdata": {"username": form_data.username, "role": user.role}
        }
    ).set_cookie(key="access_token", value=access_token, expires=int(access_token_expires.total_seconds()))


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response