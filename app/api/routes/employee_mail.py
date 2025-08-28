from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.crud.employee_crud as employee_mail_crud
import app.schemas.employee_mail as employee_mail_schema
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/send-welcome-email", dependencies=[Depends(get_current_user)])
def send_welcome_email(payload: employee_mail_schema.EmployeeMailRequest, db: Session = Depends(get_db)):
    return employee_mail_crud.send_welcome_email(db=db, request=payload)