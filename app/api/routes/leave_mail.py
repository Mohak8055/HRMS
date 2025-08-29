from fastapi import APIRouter, Depends
import app.crud.leave_mail as leave_mail_crud
import app.schemas.leave_mail as leave_mail_schema
from app.utils.auth import allow_roles

router = APIRouter()

@router.post("/send")
def send_leave_mail(payload: leave_mail_schema.LeaveMailRequest, dependencies=[Depends(allow_roles(["Admin", "Employee"]))]):
    return leave_mail_crud.send_leave_request_email(payload)