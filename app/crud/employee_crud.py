from app.schemas.employee_mail import EmployeeMailRequest
from app.utils.email import send_email, env
from sqlalchemy.orm import Session

def send_welcome_email(db: Session, request: EmployeeMailRequest):
    template = env.get_template('new_employee_welcome.html')
    html_content = template.render(
        employee_name=request.employee_name,
        temporary_password=request.temporary_password
    )
    return send_email(request.recipient_mail, request.subject, html_content)