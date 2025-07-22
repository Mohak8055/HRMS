# File: app/utils/auth.py
# --- a/file:///Users/shashishankarprasadsinha/dev/emp-fastapi/app/utils/auth.py
# +++ b/file:///Users/shashishankarprasadsinha/dev/emp-fastapi/app/utils/auth.py
# @@ -1,4 +1,5 @@
#  from datetime import datetime, timedelta
# +from typing import Optional
# from datetime import datetime, timedelta
from typing import Optional
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration (move to environment variables in production)
SECRET_KEY = "your-secret-key"  # Use a strong key in real apps
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash a plain password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify a plain password against its hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_tokens(
    data: dict,
    access_expires_delta: Optional[timedelta] = None,
    refresh_expires_delta: Optional[timedelta] = None,
) -> dict:
    to_encode = data.copy()

    # Access Token
    access_expire = datetime.utcnow() + (
        access_expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    access_token_payload = to_encode.copy()
    access_token_payload.update({"exp": access_expire, "type": "access"})
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Refresh Token
    refresh_expire = datetime.utcnow() + (
        refresh_expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    refresh_token_payload = to_encode.copy()
    refresh_token_payload.update({"exp": refresh_expire, "type": "refresh"})
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# Create a JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    print(data)
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # expire = datetime.astimezone().utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


# Decode and validate a JWT token
def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def allow_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403, detail="Access forbidden for your role"
            )
        return current_user

    return role_checker
