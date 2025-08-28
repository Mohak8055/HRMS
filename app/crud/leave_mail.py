from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
from app.schemas.leave_mail import LeaveMailRequest
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))

def create_leave_mail(request: LeaveMailRequest, html_content: str = None):
    sender_email = "stixistest@gmail.com"
    sender_password = "ucyh paym eyqx weuc"
    recipient_mail = request.recipient_mail
    subject = request.subject

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()

    try:
        smtp_server.login(sender_email, sender_password)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_mail
        message["Subject"] = subject
        
        if html_content:
            message.attach(MIMEText(html_content, "html"))
        else:
            message.attach(MIMEText(request.body, "plain"))

        smtp_server.sendmail(sender_email, recipient_mail, message.as_string())
        smtp_server.quit()
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")