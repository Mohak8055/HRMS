from fastapi import APIRouter, Depends
import app.crud.leave_mail as leave_mail
import app.schemas.leave_mail as leave_mail_schema
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/send", dependencies=[Depends(get_current_user)])
def send_leave_mail(payload: leave_mail_schema.LeaveMailRequest):
    return leave_mail.create_leave_mail(payload)