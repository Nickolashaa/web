from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.crud import user as crud_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, summary="Register new user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")

    new_user = crud_user.create_user(db=db, user=user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token, summary="Login user")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(
        db, user_credentials.login, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
