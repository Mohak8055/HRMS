from fastapi import APIRouter, Depends
from app.kafka_producer import send_message
from app.utils.auth import allow_roles
import uuid # Add this import

router = APIRouter()

@router.post("/broadcast", dependencies=[Depends(allow_roles(["Admin"]))])
async def broadcast_message(message: dict):
    # Add a unique ID and nest the original message
    message_with_id = {
        'id': str(uuid.uuid4()),
        'content': message
    }
    send_message('broadcast_messages', message_with_id)
    return {"message": "Broadcast message sent."}