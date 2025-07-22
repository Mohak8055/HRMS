from sqlalchemy.orm import Session
from app.models.department import Department
from app.models.role import Role
from app.models.userRole import user_role
from app.models.userCredential import UserCredential
from app.schemas.masterdata import DeptCreate, DeptResponse, RoleCreate, RoleResponse
from app.utils.auth import get_password_hash
from sqlalchemy import insert
from app.schemas.user import UserResponse
from sqlalchemy.orm import joinedload
from fastapi import HTTPException


def create_dept(db: Session, dept: DeptCreate):
    data = dept.model_dump()

    # Create Dept
    db_dept = Department(**data)
    db.add(db_dept)
    db.flush()  # So we can use db_user.id before commit
    db.commit()
    db.refresh(db_dept)
    # ✅ Return Pydantic response model
    return DeptResponse(id=db_dept.id, **data)


def get_depts(db: Session):
    return db.query(Department).all()


def get_dept(dept_id: int, db: Session):
    return db.query(Department).filter(Department.id == dept_id).first()


def delete_department(db: Session, dept_id: int):
    department = (
        db.query(Department)
        .filter(Department.id == dept_id, Department.active == True)
        .first()
    )
    if department:
        department.active = False
        db.commit()
        db.refresh(department)
    return department


def update_department_status(dept_id: int, active: bool, db: Session):
    department = (
        db.query(Department)
        .filter(Department.id == dept_id, Department.active == True)
        .first()
    )
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    department.active = active
    db.commit()
    db.refresh(department)
    return {
        "message": "Department status updated successfully",
        "department": DeptResponse.from_orm(department),
    }


def create_role(db: Session, role: RoleCreate):
    data = role.model_dump()

    # Create Role
    db_role = Role(**data)
    db.add(db_role)
    db.flush()  # So we can use db_user.id before commit
    db.commit()
    db.refresh(db_role)
    # ✅ Return Pydantic response model
    return DeptResponse(id=db_role.id, **data)


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(role_id: int, db: Session):
    return db.query(Role).filter(Role.id == role_id).first()


def delete_role(db: Session, role_id: int):
    role = db.query(Role).filter(Role.id == role_id, Role.active == True).first()
    if role:
        role.active = False
        db.commit()
        db.refresh(role)
    return role


def update_role_status(role_id: int, active: bool, db: Session):
    role = db.query(Role).filter(Role.id == role_id, Role.active == True).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.active = active
    db.commit()
    db.refresh(role)
    return {
        "message": "Department status updated successfully",
        "role": RoleResponse.from_orm(role),
    }
