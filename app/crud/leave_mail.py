from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
import app.schemas.leave_mail as leave_mail_schema



def create_leave_mail(request: leave_mail_schema.LeaveMailRequest):
    sender_email = "stixistest@gmail.com"
    sender_password = "ucyh paym eyqx weuc"
    recipient_mail = request.recipient_mail
    subject = request.subject
    body = request.body

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()

    try:
        smtp_server.login(sender_email, sender_password)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_mail
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        smtp_server.sendmail(sender_email, recipient_mail, message.as_string())
        smtp_server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")
