# kafka_consumer.py

from kafka import KafkaConsumer
import json
import base64
from app.crud.user import create_user
from app.database import SessionLocal
from app.schemas.user import UserCreate
import openpyxl
import io
from app.crud.employee_crud import send_welcome_email
from app.schemas.employee_mail import EmployeeMailRequest

def process_bulk_creation():
    consumer = KafkaConsumer(
        'employee_bulk_creation',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='employee-creation-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    db = SessionLocal()

    for message in consumer:
        file_data = message.value
        file_content = base64.b64decode(file_data['file_content'])
        
        workbook = openpyxl.load_workbook(io.BytesIO(file_content))
        sheet = workbook.active

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):
                continue
            try:
                phone_number = str(int(row[1])) if row[1] is not None else None
                
                user_data = UserCreate(
                    email=row[0],
                    phone=phone_number,
                    firstName=row[2],
                    lastName=row[3],
                    dob=row[4],
                    doj=row[5],
                    departmentId=row[6],
                    roleId=row[7],
                    password=row[8]
                )
                
                # Create user in the database
                created_user = create_user(db, user_data)

                # Send welcome email for each new user
                email_payload = EmployeeMailRequest(
                    recipient_mail=created_user.email,
                    subject='Welcome to the Team! Your Login Credentials',
                    employee_name=f"{created_user.firstName} {created_user.lastName}",
                    temporary_password=row[8] # The password from the excel file
                )
                send_welcome_email(db, email_payload)
                print(f"Processed and sent email for {created_user.email}")

            except Exception as e:
                print(f"Error processing row {row_idx}: {e}")

if __name__ == "__main__":
    process_bulk_creation()