from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List

# Configuration
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_tokens(data: dict, access_expires_delta: Optional[timedelta] = None, refresh_expires_delta: Optional[timedelta] = None) -> dict:
    to_encode = data.copy()

    access_expire = datetime.utcnow() + (access_expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token_payload = to_encode.copy()
    access_token_payload.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_expire = datetime.utcnow() + (refresh_expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    refresh_token_payload = to_encode.copy()
    refresh_token_payload.update({"exp": refresh_expire, "type": "refresh"})
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("userId")
        roles: list = payload.get("roles")
        if user_id is None or roles is None:
            raise credentials_exception
        return {"user_id": user_id, "roles": roles}
    except JWTError:
        raise credentials_exception

def allow_roles(allowed_roles: List[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_roles = [role["name"] for role in current_user["roles"]]
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Access forbidden for your role"
            )
        return current_user
    return role_checker