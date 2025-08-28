from pydantic import BaseModel, EmailStr

class EmployeeMailRequest(BaseModel):
    recipient_mail: EmailStr
    subject: str
    employee_name: str
    temporary_password: str