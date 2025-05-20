from datetime import datetime, timedelta, timezone
from typing import Tuple
from passlib.context import CryptContext
from jose import jwt, JWTError
from uuid import UUID
from sqlalchemy.orm import Session
from src.core.config import settings
from src.entities.models import User, Roles
from .schemas import RegisterUserRequest, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS))
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def register_user(db: Session, payload: RegisterUserRequest) -> User:
    user = User(
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        password_hash=hash_password(payload.password),
        role=Roles.BUYER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Tuple[User, Token]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None, None

    access_token = create_access_token({"sub": str(user.user_id)})
    refresh_token = create_refresh_token({"sub": str(user.user_id)})
    
    return user, Token(access_token=access_token, refresh_token=refresh_token)
    
def verify_refresh_token(refresh_token: str) -> Token | None:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        # Create a new access token
        access_token = create_access_token({"sub": user_id})
        # Optionally create a new refresh token, or just return the old one
        new_refresh_token = create_refresh_token({"sub": user_id})
        return Token(access_token=access_token, refresh_token=new_refresh_token)
    except JWTError:
        return None

