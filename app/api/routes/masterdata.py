from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.masterdata import DeptResponse, DeptCreate, RoleResponse, RoleCreate
from app.crud.masterdata import (
    create_dept,
    create_role,
    get_depts,
    get_dept,
    delete_department,
    update_department_status,
    get_role,
    delete_role,
    update_role_status,
    get_roles,
)
from typing import List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add-dept", response_model=DeptResponse)
def create(dept: DeptCreate, db: Session = Depends(get_db)):
    return create_dept(db, dept)


@router.get("/depts", response_model=List[DeptResponse])
def list_depts(db: Session = Depends(get_db)):
    return get_depts(db)


@router.get("/dept/{id}", response_model=DeptResponse)
def dept(id: int, db: Session = Depends(get_db)):
    return get_dept(id, db)


@router.delete("/dept/{id}", response_model=DeptResponse)
def list_users(db: Session = Depends(get_db)):
    return delete_department(db)


@router.patch("/department/{dept_id}/status")
def update_dept_status(dept_id: int, active: bool, db: Session = Depends(get_db)):
    return update_department_status(dept_id, active, db)


@router.post("/add-role", response_model=RoleResponse)
def create(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)


@router.get("/roles", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.get("/role/{id}", response_model=RoleResponse)
def role(id: int, db: Session = Depends(get_db)):
    return get_role(id, db)


@router.delete("/role/{id}", response_model=List[DeptResponse])
def delete_role(db: Session = Depends(get_db)):
    return delete_role(db)


@router.patch("/role/{role_id}/status")
def update_role_status(role_id: int, active: bool, db: Session = Depends(get_db)):
    return update_role_status(role_id, active, db)
