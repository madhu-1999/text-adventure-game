from datetime import datetime, timedelta, timezone
import os
from typing import Any, Optional, Union
import bcrypt
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))

def get_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password=password.encode(), salt=salt)
    return hashed.decode()

def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_pass.encode())

def create_access_token(subject: Union[str, Any], expires_delta: Optional[int] = None) -> str:
    if expires_delta is not None:
        expires = int((datetime.now(timezone.utc) + timedelta(seconds=expires_delta)).timestamp())
    else:
        expires = int((datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())

    to_encode = {"exp": expires, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
