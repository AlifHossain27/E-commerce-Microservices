from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.middlewares.rate_limiting import limiter
from src.database.db import DbSession
from src.auth.schemas import RegisterUserRequest, LoginRequest, Token, RefreshTokenRequest
from src.auth.services import register_user, authenticate_user, create_access_token, create_refresh_token, verify_refresh_token
from src.exceptions.handlers import ConflictException, UnauthorizedException

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=Token)
@limiter.limit("5/minute")
def register(request: Request, payload: RegisterUserRequest, db: DbSession):
    from src.entities.models import User

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise ConflictException(detail="Email is already registered.")
    
    user = register_user(db, payload)
    tokens = authenticate_user(db, user.email, payload.password)[1]
    return tokens

@auth_router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginRequest, db: DbSession):
    user, tokens = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise UnauthorizedException(detail="Invalid email or password.")
    return tokens

@auth_router.post("/refresh", response_model=Token)
def refresh_token(request: Request, payload: RefreshTokenRequest):
    # payload contains the refresh_token string
    new_access_token = verify_refresh_token(payload.refresh_token)
    if not new_access_token:
        raise UnauthorizedException(detail="Invalid refresh token.")
    return new_access_token
