from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))

def send_email(recipient_mail: str, subject: str, html_content: str):
    # --- START: Update with your Mailtrap credentials ---
    sender_email = "d23756b3c1d156"
    sender_password = "9a1d46c095edda"

    smtp_host = "sandbox.smtp.mailtrap.io"
    smtp_port = 2525
    # --- END: Update with your Mailtrap credentials ---

    smtp_server = smtplib.SMTP(smtp_host, smtp_port)
    smtp_server.starttls()

    try:
        smtp_server.login(sender_email, sender_password)
        message = MIMEMultipart()
        message["From"] = "HR Department <donotreply@hrms.com>"
        message["To"] = recipient_mail
        message["Subject"] = subject
        message.attach(MIMEText(html_content, "html"))

        smtp_server.sendmail(message["From"], recipient_mail, message.as_string())
        smtp_server.quit()
        return {"message": "Email sent successfully to Mailtrap"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {e}")