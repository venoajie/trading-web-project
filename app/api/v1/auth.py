
# trading_app/app/api/v1/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user as user_schema
from app.schemas import token as token_schema
from app.crud import crud_user
from app.core import security
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=user_schema.UserRead)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: user_schema.UserCreate,
):
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await crud_user.create_user(db=db, user_in=user_in)
    return user

@router.post("/login", response_model=token_schema.Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}