from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserPasswordUpdate
from app.crud.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    toggle_user_activation,
    update_user_password,
    bulk_create_users,
)
from app.utils.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/bulk-create", dependencies=[Depends(get_current_user)])
async def bulk_create(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")
    
    return await bulk_create_users(db, file)

@router.post("/create", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/all-user", dependencies=[Depends(get_current_user)])
def list_users(
    email: Optional[str] = Query(None),
    phone: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    active: Optional[bool] = Query(None),
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=0),
    db: Session = Depends(get_db),
):
    return get_users(
        db,
        email=email,
        phone=phone,
        name=name,
        department=department,
        role=role,
        active=active,
        limit=limit,
        page=page,
    )

@router.get("/{id}", response_model=UserResponse, dependencies=[Depends(get_current_user)])
def find_user(id: int, db: Session = Depends(get_db)):
    user = get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        **user.__dict__,
        email=user.credential.email if user.credential else "",
        roleId=user.roles[0].id if user.roles else None,
    )

@router.put("/update", response_model=UserUpdate)
def update(user_data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_data)

@router.patch("/reset-password")
def reset_password(user_pass: UserPasswordUpdate, db: Session = Depends(get_db)):
    return update_user_password(db, user_pass)

@router.delete("/{id}/{status}")
def delete_user(id: int, status: bool, db: Session = Depends(get_db)):
    return toggle_user_activation(id, status, db)