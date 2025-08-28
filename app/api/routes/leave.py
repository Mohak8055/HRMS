from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.leave import LeaveResponse, LeaveCreate, LeaveUpdate
from app.crud import leave as leave_crud
from typing import List

from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=LeaveResponse, dependencies=[Depends(get_current_user)])
def create_leave(leave: LeaveCreate, db: Session = Depends(get_db)):
    return leave_crud.create_leave(db=db, leave=leave)

@router.get("/user/{user_id}", response_model=List[LeaveResponse], dependencies=[Depends(get_current_user)])
def read_leaves_by_user(user_id: int, db: Session = Depends(get_db)):
    leaves = leave_crud.get_leaves_by_user(db, user_id=user_id)
    return leaves

@router.get("/", response_model=List[LeaveResponse], dependencies=[Depends(get_current_user)])
def read_all_leaves(db: Session = Depends(get_db)):
    leaves = leave_crud.get_all_leaves(db)
    return leaves

@router.patch("/{leave_id}", response_model=LeaveResponse, dependencies=[Depends(get_current_user)])
def update_leave_status(leave_id: int, status: LeaveUpdate, db: Session = Depends(get_db)):
    updated_leave = leave_crud.update_leave_status(db, leave_id=leave_id, status=status)
    if updated_leave is None:
        raise HTTPException(status_code=404, detail="Leave not found")
    return updated_leave