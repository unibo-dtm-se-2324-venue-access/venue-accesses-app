from datetime import timedelta
import datetime
from typing import Optional
from fastapi import Depends, Request, status, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status


SECRET_KEY_JWT = "b9aeb1ac75e5a78ff68e0f7966c9e8a4e389fbe64a7b31e4e30b88b1141d2089"
ALGORITHM_JWT= "HS256"

class TokenData(BaseModel):
  username: str
  role: str | None

def cookie_extractor(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token not found")
    return token 

def get_current_manager(token: str = Depends(cookie_extractor)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM_JWT])
        username: str = payload.get("email")
        role: str = payload.get("role")
        if username is None or role not in ['CEO','HR']:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError as e:
        print("JWT decoding failed:", str(e))
        raise credentials_exception

    return token_data

def get_current_employee(token: str = Depends(cookie_extractor)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM_JWT])
        username: str = payload.get("email")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError as e:
        print("JWT decoding failed:", str(e))
        raise credentials_exception

    return token_data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data.pop('user_password', None) 
    to_encode = data.copy()

    for key, value in to_encode.items():
        if isinstance(value, datetime.date):
            to_encode[key] = value.isoformat()

    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM_JWT)
    return encoded_jwt