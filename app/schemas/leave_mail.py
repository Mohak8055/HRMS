from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class LeaveMailRequest(BaseModel):
    recipient_mail: EmailStr
    subject: str
    body: Dict[str, Any]