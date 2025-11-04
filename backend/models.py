from pydantic import BaseModel, EmailStr
from typing import Optional, List

class SignupModel(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = ""
    age: Optional[int] = None
    bio: Optional[str] = ""

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class ResetRequestModel(BaseModel):
    email: EmailStr

class ResetConfirmModel(BaseModel):
    email: EmailStr
    token: str
    new_password: str

class SingleText(BaseModel):
    text: str


class ProfileUpdate(BaseModel):
    email: str
    full_name: str
    age: int
    bio: str