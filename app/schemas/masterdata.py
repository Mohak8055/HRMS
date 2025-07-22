from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import date, datetime


class RoleBase(BaseModel):
    name: str = constr(max_length=15)
    alias: str = constr(max_length=50)
    active: Optional[bool] = True  # New field added
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class RoleCreate(RoleBase):
    pass  # You can add password or registration-specific fields here


class RoleUpdate(RoleBase):
    pass


# For reading from DB, with internal ID
class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


# ✅ Final response schema — safe for public API output
class RoleResponse(RoleInDBBase):
    class Config:
        from_attributes = True


class DeptBase(BaseModel):
    name: str = constr(max_length=15)
    description: str = constr(max_length=50)
    active: Optional[bool] = True  # New field added
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None


class DeptCreate(DeptBase):
    pass


class DeptUpdate(DeptBase):
    pass


# For reading from DB, with internal ID
class DeptInDBBase(DeptBase):
    id: int

    class Config:
        from_attributes = True


# ✅ Final response schema — safe for public API output
class DeptResponse(DeptInDBBase):
    class Config:
        from_attributes = True
