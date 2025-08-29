from app.schemas.leave_mail import LeaveMailRequest
from app.utils.email import send_email, env
from datetime import datetime

def format_date(date_string):
    if not date_string:
        return ""
    # Parse the ISO format string and reformat it
    dt_object = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    return dt_object.strftime('%d-%b-%Y')

def send_leave_request_email(request: LeaveMailRequest):
    template = env.get_template('leave_request.html')
    html_content = template.render(
        leave_type=request.body.get("leave_type"),
        from_date=format_date(request.body.get("from_date")),
        to_date=format_date(request.body.get("to_date")),
        contact_details=request.body.get("contact_details"),
        reason=request.body.get("reason"),
        employee_name=request.body.get("employee_name")
    )
    return send_email(request.recipient_mail, request.subject, html_content)