from pydantic import BaseModel, Field
from datetime import datetime
from .models import UserRole


class UserResponse(BaseModel):
    id: int 
    username: str 
    email: str 
    password: str = Field(exclude=True)
    role: UserRole
    is_active: bool
    created_date : datetime




class Create_User_model(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(min_length=6, max_length=12)
    role: UserRole = Field(default=UserRole.User,) 
    is_active: bool = Field(default=True, nullable=False)
    created_date : datetime 


class User_Login_Model(BaseModel):
    email: str = Field(max_length=100)
    password: str = Field(min_length=6, max_length=12)