# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     email: str
#     name: str

# class UserResponse(UserCreate):
#     id: int

#     class Config:
#         from_attributes = True


from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional, Annotated
from datetime import date, datetime
from app.schemas.masterdata import RoleResponse, DeptResponse


class UserBase(BaseModel):
    email: EmailStr
    phone: Annotated[str, Field(max_length=15)]
    firstName: str
    lastName: str
    dob: date  # Accepts 'YYYY-MM-DD' format
    doj: date  # Accepts 'YYYY-MM-DD' format
    departmentId: Optional[int] = None
    managerId: Optional[int] = None
    active: Optional[bool] = True  # New field added
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class UserCreate(UserBase):
    password: str = constr(min_length=6)  # Add password validation
    roleId: int
    pass  # You can add password or registration-specific fields here


# For updating user details, excluding password


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
    # roleId: Optional[int] = None


# For reading from DB, with internal ID
class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True


# ✅ Final response schema — safe for public API output
class UserResponse(UserInDBBase):
    roleId: int  # Optional: include only if needed

    class Config:
        from_attributes = True


class AllUserResponse(UserInDBBase):
    roleId: int  # Optional: include only if needed
    role: Optional[dict]
    department: Optional[dict]

    class Config:
        from_attributes = True
