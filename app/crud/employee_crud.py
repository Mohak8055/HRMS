from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
import os
from app.schemas.employee_mail import EmployeeMailRequest
from app.crud.leave_mail import create_leave_mail
from sqlalchemy.orm import Session

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))

def send_welcome_email(db: Session, request: EmployeeMailRequest):
    try:
        template = env.get_template('new_employee_welcome.html')
        html_content = template.render(
            employee_name=request.employee_name,
            temporary_password=request.temporary_password
        )
        
        # Re-use the existing email sending logic
        return create_leave_mail(request, html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering email template: {e}")