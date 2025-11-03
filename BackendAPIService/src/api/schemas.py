from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Auth Schemas
class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type (bearer)")


class TokenData(BaseModel):
    user_id: int
    email: EmailStr
    is_admin: bool = False


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password for the new user")


class UserLogin(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# Post Schemas
class PostBase(BaseModel):
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content")
    topic: Optional[str] = Field(None, description="Topic or keyword")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    topic: Optional[str] = None


class PostOut(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    version: int

    class Config:
        from_attributes = True


class PostVersionOut(BaseModel):
    id: int
    post_id: int
    version_number: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# Generation
class GenerateRequest(BaseModel):
    topic: str = Field(..., description="Topic or keywords for blog generation")
    style: Optional[str] = Field(None, description="Optional style instructions")


class GenerateResponse(BaseModel):
    title: str
    content: str


# Export
class ExportResponse(BaseModel):
    export_type: str
    content: str
    note: Optional[str] = None
