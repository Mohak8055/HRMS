from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud.user import (
    create_user,
    get_users,
    get_user,
    update_user,
    toggle_user_activation,
)
from typing import List

from app.utils.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=UserResponse, dependencies=[Depends(get_current_user)])
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


@router.put("/update", response_model=UserUpdate, dependencies=[Depends(get_current_user)])
def update(user_data: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_data)


@router.delete("/{id}/{status}", dependencies=[Depends(get_current_user)])
def delete_user(id: int, status: bool, db: Session = Depends(get_db)):
    return toggle_user_activation(id, status, db)
