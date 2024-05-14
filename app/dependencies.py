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
    # Extract 'access_token' from cookies
    token = request.cookies.get("access_token")
    if not token:
        # If token is missing, raise an HTTP 401 Unauthorized exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token not found")
    return token 

def get_current_manager(token: str = Depends(cookie_extractor)):
    # Decode the JWT token to get the user's information
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM_JWT])
        username: str = payload.get("email")
        role: str = payload.get("role")
        # Validate username presence
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Check if the role is either CEO or HR
        if role not in ['CEO', 'HR']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username, role=role)
    except JWTError as e:
        print("JWT decoding failed:", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def get_current_employee(token: str = Depends(cookie_extractor)):
    # Predefined HTTP exception for credential errors
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM_JWT])
        username: str = payload.get("email")
        role: str = payload.get("role")
        # Ensure the username is present
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
    except JWTError as e:
        print("JWT decoding failed:", str(e))
        raise credentials_exception

    return token_data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Remove user password from data if present
    data.pop('user_password', None) 
    to_encode = data.copy()

    # Convert datetime.date to ISO format if any date is present
    for key, value in to_encode.items():
        if isinstance(value, datetime.date):
            to_encode[key] = value.isoformat()

    # Set expiration for the token
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=30)

    # Add expiration timestamp to the payload
    to_encode.update({"exp": int(expire.timestamp())})

    # Encode the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_JWT, algorithm=ALGORITHM_JWT)
    return encoded_jwt
