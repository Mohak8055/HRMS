from datetime import datetime
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.userprofile import ProfilePhoto
from app.models.user import User
from fastapi.responses import JSONResponse

from app.utils.auth import allow_roles

UPLOAD_DIR = "uploads/profile_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def generate_unique_filename(user_id: int, original_filename: str) -> str:
    """Generate a unique filename with UUID or timestamp while keeping file extension."""
    file_ext = os.path.splitext(original_filename)[1]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]  # short UUID
    return f"user_{user_id}_{timestamp}_{unique_id}{file_ext}"

@router.post("/upload-profile-photo", dependencies=[Depends(allow_roles(["Admin", "Employee"]))])
async def upload_profile_photo(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_name = generate_unique_filename(user_id, file.filename)
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save new file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # If previous photo exists, delete it
    photo_record = db.query(ProfilePhoto).filter(ProfilePhoto.user_id == user_id).first()
    if photo_record and os.path.exists(photo_record.file_path):
        os.remove(photo_record.file_path)

    # Update DB record
    if photo_record:
        photo_record.file_name = file_name
        photo_record.file_path = file_path
    else:
        photo_record = ProfilePhoto(user_id=user_id, file_name=file_name, file_path=file_path)
        db.add(photo_record)

    db.commit()

    # ✅ The filename itself is unique, so cache-busting param isn’t even necessary
    file_url = f"/profile-photos/{file_name}"

    return JSONResponse(content={
        "message": "Profile photo uploaded successfully",
        "file_url": file_url,
        "file_path": file_path
    })

@router.get("/get-profile-photo/{user_id}", dependencies=[Depends(allow_roles(["Admin", "Employee"]))])
def get_profile_photo(user_id: int, db: Session = Depends(get_db)):
    photo_record = db.query(ProfilePhoto).filter(ProfilePhoto.user_id == user_id).first()
    if not photo_record:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    # Relative URL
    photo_url = f"/profile-photos/{photo_record.file_name}"

    return {
        "user_id": user_id,
        "file_name": photo_record.file_name,
        "file_path": photo_record.file_path,  # local path
        "file_url": photo_url,  # relative URL
    }


@router.put("/update-profile-photo/{user_id}", dependencies=[Depends(allow_roles(["Admin", "Employee"]))])
async def update_profile_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_name = generate_unique_filename(user_id, file.filename)
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Save new file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Delete old file if exists
    photo_record = db.query(ProfilePhoto).filter(ProfilePhoto.user_id == user_id).first()
    if photo_record and os.path.exists(photo_record.file_path):
        os.remove(photo_record.file_path)

    # Update DB record
    if photo_record:
        photo_record.file_name = file_name
        photo_record.file_path = file_path
    else:
        photo_record = ProfilePhoto(user_id=user_id, file_name=file_name, file_path=file_path)
        db.add(photo_record)

    db.commit()

    # ✅ Always latest unique file URL
    file_url = f"/profile-photos/{file_name}"

    return JSONResponse(content={
        "message": "Profile photo updated successfully",
        "file_url": file_url,
        "file_path": file_path
    })
@router.delete("/remove-profile-photo/{user_id}", dependencies=[Depends(allow_roles(["Admin", "Employee"]))])
def remove_profile_photo(user_id: int, db: Session = Depends(get_db)):
    photo_record = db.query(ProfilePhoto).filter(ProfilePhoto.user_id == user_id).first()
    if not photo_record:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    if os.path.exists(photo_record.file_path):
        os.remove(photo_record.file_path)

    db.delete(photo_record)
    db.commit()

    return JSONResponse(content={"message": "Profile photo removed successfully"})
