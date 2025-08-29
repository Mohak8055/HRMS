from pydantic import BaseModel
from datetime import date
from typing import Optional, TYPE_CHECKING

# This block helps with type hinting without causing runtime circular imports
if TYPE_CHECKING:
    from app.schemas.user import UserSimpleResponse

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
    # Use a string "forward reference" to avoid direct import at the class definition level
    user: Optional["UserSimpleResponse"] = None

    class Config:
        from_attributes = True

# Import the schema here and rebuild the model to resolve the forward reference
from app.schemas.user import UserSimpleResponse
LeaveResponse.model_rebuild()