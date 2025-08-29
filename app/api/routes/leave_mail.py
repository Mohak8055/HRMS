from fastapi import APIRouter
import app.crud.leave_mail as leave_mail_crud
import app.schemas.leave_mail as leave_mail_schema

router = APIRouter()

@router.post("/send")
def send_leave_mail(payload: leave_mail_schema.LeaveMailRequest):
    return leave_mail_crud.send_leave_request_email(payload)