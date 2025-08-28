from pydantic import BaseModel
from datetime import date
from typing import Optional
from app.schemas.user import UserSimpleResponse # Import the new schema

class LeaveBase(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str

class LeaveCreate(LeaveBase):
    user_id: int

class LeaveUpdate(BaseModel):
    status: str

class LeaveResponse(LeaveBase):
    id: int
    user_id: int
    status: str
    user: Optional[UserSimpleResponse] = None # Add this line

    class Config:
        from_attributes = True