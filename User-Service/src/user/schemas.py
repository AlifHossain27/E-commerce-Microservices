from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from enum import Enum
from typing import Optional
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    seller = "seller"
    buyer = "buyer"

class AddressBase(BaseModel):
    full_address: str
    postal_code: str
    city: str
    country: str

class Address(AddressBase):
    address_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str]
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    address: Optional[AddressBase]

class User(UserBase):
    user_id: UUID
    address: Optional[AddressBase]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangePassword(BaseModel):
    old_password: str
    new_password: str


