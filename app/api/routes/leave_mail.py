from fastapi import APIRouter, Depends
import app.crud.leave_mail as leave_mail
import app.schemas.leave_mail as leave_mail_schema

router = APIRouter()

@router.post("/send")
def send_leave_mail(payload: leave_mail_schema.LeaveMailRequest):
    return leave_mail.create_leave_mail(payload)