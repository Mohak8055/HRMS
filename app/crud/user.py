from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.user import User
from app.models.userRole import user_role
from app.models.userCredential import UserCredential
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from app.utils.auth import get_password_hash, verify_password
from sqlalchemy import insert
from datetime import datetime
from app.schemas.user import UserResponse, AllUserResponse
from sqlalchemy.orm import joinedload
from typing import Optional
from app.models.department import Department
from app.models.role import Role


def create_user(db: Session, user: UserCreate):
    data = user.model_dump()

    # Clean up foreign keys: convert 0 to None
    if data.get("departmentId") == 0:
        data["departmentId"] = None
    if data.get("managerId") == 0:
        data["managerId"] = None

    # Extract sensitive or separate fields
    email = data.pop("email")
    phone = data["phone"]
    plain_password = data.pop("password")
    role_id = data.pop("roleId")
    # 🔍 Check if email already exists
    email_exists = db.query(UserCredential).filter_by(email=email).first()
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    # 🔍 Check if phone already exists
    phone_exists = db.query(User).filter_by(phone=phone).first()
    if phone_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number already exists",
        )
    # Create User
    db_user = User(**data)
    db.add(db_user)
    db.flush()  # So we can use db_user.id before commit

    # Create UserCredential
    hashed_password = get_password_hash(plain_password)
    credential = UserCredential(
        userId=db_user.id, email=email, hashedPassword=hashed_password
    )
    db.add(credential)

    # Insert into UserRole association table
    db.execute(insert(user_role).values(userId=db_user.id, roleId=role_id))

    db.commit()
    db.refresh(db_user)
    print(type(db_user))
    # ✅ Return Pydantic response model
    return UserResponse(id=db_user.id, email=email, roleId=role_id, **data)


def get_users(
    db: Session,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    name: Optional[str] = None,
    department: Optional[str] = None,
    role: Optional[str] = None,
    active: Optional[bool] = None,
    limit: int = 10,
    page: int = 1,
):
    offset = (page - 1) * limit
    base_query = db.query(User)

    if name:
        parts = name.strip().split()
        if len(parts) == 1:
            search = f"%{parts[0]}%"
            base_query = base_query.filter(
                or_(User.firstName.ilike(search), User.lastName.ilike(search))
            )
        elif len(parts) >= 2:
            first = f"%{parts[0]}%"
            last = f"%{parts[1]}%"
            base_query = base_query.filter(
                and_(User.firstName.ilike(first), User.lastName.ilike(last))
            )
    if email:
        base_query = base_query.filter(
            User.credential.has(UserCredential.email.ilike(f"%{email}%"))
        )
    if phone:
        base_query = base_query.filter(User.phone.ilike(f"%{phone}%"))
    if department:
        base_query = base_query.filter(
            User.department.has(Department.name.ilike(f"%{department}%"))
        )
    if active is not None:
        base_query = base_query.filter(User.active == active)
    if role:
        base_query = base_query.filter(User.roles.any(Role.name.ilike(f"%{role}%")))

    total = base_query.count()
    page = (offset // limit) + 1 if limit > 0 else 1

    users = (
        base_query.options(
            joinedload(User.credential),
            joinedload(User.roles),
            joinedload(User.department),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for user in users:
        email = user.credential.email if user.credential else None
        role = (
            {"id": user.roles[0].id, "name": user.roles[0].name} if user.roles else None
        )
        department = (
            {"id": user.department.id, "name": user.department.name}
            if user.department
            else None
        )

        user_data = AllUserResponse(
            id=user.id,
            email=email,
            phone=user.phone,
            firstName=user.firstName,
            lastName=user.lastName,
            dob=user.dob,
            doj=user.doj,
            departmentId=user.departmentId,
            managerId=user.managerId,
            active=user.active,
            createdAt=user.createdAt,
            updatedAt=user.updatedAt,
            role=role,
            roleId=user.roles[0].id if user.roles else None,
            department=department,
        )
        result.append(user_data)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "page": page,
        "users": result,
    }


def get_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user if user else None


def update_user(db: Session, user: UserUpdate):
    data = user.model_dump(exclude_unset=True)

    if "departmentId" in data and data["departmentId"] == 0:
        data["departmentId"] = None
    if "managerId" in data and data["managerId"] == 0:
        data["managerId"] = None

    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    if "email" in data:
        db_cred = (
            db.query(UserCredential).filter(UserCredential.userId == user.id).first()
        )
        if db_cred:
            db_cred.email = data["email"]

    db_user.updatedAt = datetime.utcnow()

    db.commit()
    db.refresh(db_user)

    return UserUpdate(
        email=db_user.credential.email if db_user.credential else None,
        **{k: getattr(db_user, k) for k in data if hasattr(db_user, k)},
    )

def update_user_password(db: Session, user_pass: UserPasswordUpdate):
    db_cred = db.query(UserCredential).filter(UserCredential.userId == user_pass.id).first()
    if not db_cred or not verify_password(user_pass.old_password, db_cred.hashedPassword):
        raise HTTPException(status_code=400, detail="Invalid old password")

    db_cred.hashedPassword = get_password_hash(user_pass.new_password)
    db.commit()
    return {"message": "Password updated successfully"}


def toggle_user_activation(user_id: int, activate: bool, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.active = activate
    user.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return {"Message": "User status updated successfully", "status": user.active}