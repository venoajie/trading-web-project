
# trading_app/app/schemas/user.py
import uuid
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to client
class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True # Replaces orm_mode=True