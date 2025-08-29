from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))

def send_email(recipient_mail: str, subject: str, html_content: str):
    sender_email = "stixistest@gmail.com"
    sender_password = "ucyh paym eyqx weuc"

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()

    try:
        smtp_server.login(sender_email, sender_password)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_mail
        message["Subject"] = subject
        message.attach(MIMEText(html_content, "html"))

        smtp_server.sendmail(sender_email, recipient_mail, message.as_string())
        smtp_server.quit()
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")