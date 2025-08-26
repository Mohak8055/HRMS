from pydantic import BaseModel, EmailStr
from typing import Optional


class LeaveMailRequest(BaseModel):
    recipient_mail: EmailStr
    subject: str
    body: str
