from pydantic import BaseModel
from fastapi import Field
from datetime import datetime
from .models import UserRole

class Create_User_model(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100)
    # password: str = Field(exclude=True)
    password: str = Field(min_length=6, max_length=12)
    role: UserRole = Field(default=UserRole.User,) 
    is_active: bool = Field(default=True, nullable=False)
    created_date : datetime 