from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# Request schema for user registration
class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

# Request schema for login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Token payload
class TokenData(BaseModel):
    user_id: str | None = None

    def get_uuid(self) -> UUID | None:
        return UUID(self.user_id) if self.user_id else None

class RefreshTokenRequest(BaseModel):
    refresh_token: str