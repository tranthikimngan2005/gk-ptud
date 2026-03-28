from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- Schema cho User (Đăng ký/Đăng nhập) ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Schema cho Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Schema cho Photo (Đề bài yêu cầu) ---
class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None

class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id: int
    image_url: str
    uploaded_at: datetime
    user_id: int

    class Config:
        from_attributes = True