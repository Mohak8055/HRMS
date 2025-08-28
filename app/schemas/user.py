from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, Annotated
from datetime import date, datetime
from app.schemas.masterdata import RoleResponse, DeptResponse


class UserBase(BaseModel):
    email: EmailStr
    phone: Annotated[str, Field(max_length=15)]
    firstName: str
    lastName: str
    dob: date
    doj: date
    departmentId: Optional[int] = None
    managerId: Optional[int] = None
    active: Optional[bool] = True
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class UserCreate(UserBase):
    password: str = constr(min_length=6)
    roleId: int


class UserUpdate(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    phone: Optional[Annotated[str, Field(max_length=15)]] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    departmentId: Optional[int] = None
    managerId: Optional[int] = None
    active: Optional[bool] = None
    updatedAt: Optional[datetime] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(UserInDBBase):
    roleId: int

    class Config:
        from_attributes = True


class AllUserResponse(UserInDBBase):
    roleId: int
    role: Optional[dict]
    department: Optional[dict]

    class Config:
        from_attributes = True


class UserSimpleResponse(BaseModel):
    id: int
    firstName: str
    lastName: str

    class Config:
        from_attributes = True

class UserPasswordUpdate(BaseModel):
    id: int
    old_password: str
    new_password: str