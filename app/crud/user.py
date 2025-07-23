from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.user import User
from app.models.userRole import user_role
from app.models.userCredential import UserCredential
from app.schemas.user import UserCreate, UserUpdate
from app.utils.auth import get_password_hash
from sqlalchemy import insert
from datetime import datetime
from app.schemas.user import UserResponse, AllUserResponse
from sqlalchemy.orm import joinedload
from typing import Optional
from app.models.department import Department
from app.models.role import Role


def create_user_old(db: Session, user: UserCreate):

    # db_user = User(**user.model_dump(exclude={"password","email","roleId"}))
    data = user.model_dump()

    # Clean up foreign keys: convert 0 to None
    if data.get("departmentId") == 0:
        data["departmentId"] = None
    if data.get("managerId") == 0:
        data["managerId"] = None

    # Extract and remove email and password from user payload
    email = data.pop("email")
    plain_password = data.pop("password")
    role_id = data.pop("roleId")
    # Create User
    db_user = User(**data)
    db.add(db_user)
    db.flush()  # Get db_user.id
    # Create credentials
    hashPassword = get_password_hash(plain_password)
    credential = UserCredential(
        userId=db_user.id, email=email, hashedPassword=hashPassword
    )
    db.add(credential)
    # Insert into UserRole
    db.execute(insert(user_role).values(userId=db_user.id, roleId=role_id))

    db.commit()
    db.refresh(db_user)
    db_user = User(**data)
    db.add(db_user)  # Add the user to the session
    db.flush()  # Ensure the user is added to the session before committing
    credentail = UserCredential(
        userId=db_user.id, email=user.email, hashedPassword=hashPassword
    )

    db.add(credentail)
    db.commit()
    db.refresh(db_user)
    print(db_user)
    return db_user


def create_user(db: Session, user: UserCreate):
    data = user.model_dump()

    # Clean up foreign keys: convert 0 to None
    if data.get("departmentId") == 0:
        data["departmentId"] = None
    if data.get("managerId") == 0:
        data["managerId"] = None

    # Extract sensitive or separate fields
    email = data.pop("email")
    plain_password = data.pop("password")
    role_id = data.pop("roleId")

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
    # query = db.query(User).options(
    #     joinedload(User.credential),
    #     joinedload(User.roles),
    #     joinedload(User.department),
    # )
    if name:
        parts = name.strip().split()
        if len(parts) == 1:
            search = f"%{parts[0]}%"
            base_query = base_query.filter(or_(
                User.firstName.ilike(search),
                User.lastName.ilike(search)
            ))
        elif len(parts) >= 2:
            first = f"%{parts[0]}%"
            last = f"%{parts[1]}%"
            base_query = base_query.filter(and_(
                User.firstName.ilike(first),
                User.lastName.ilike(last)
            ))
    if email:
        base_query = base_query.filter(
            User.credential.has(UserCredential.email.ilike(f"%{email}%"))
        )
    if phone:
        # query = query.filter(User.phone == phone)
        base_query = base_query.filter(User.phone.ilike(f"%{phone}%"))
    if department:
        base_query = base_query.filter(
            User.department.has(Department.name.ilike(f"%{department}%"))
        )
    if active is not None:
        base_query = base_query.filter(User.active == active)
    if role:
        base_query = base_query.filter(User.roles.any(Role.name.ilike(f"%{role}%")))
    # Total count (no offset/limit, no joinedload needed)
    total = base_query.count()
    page = (offset // limit) + 1 if limit > 0 else 1
    # Fetch paginated data with joined relationships
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

    # users = query.offset(offset).limit(limit).all()
    # users = query.all()
    result = []
    # return users
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

        # role = (
        #     RoleResponse(id=user.roles[0].id, name=user.roles[0].name)
        #     if user.roles
        #     else None
        # )
        # department = (
        #     DeptResponse(id=user.department.id, name=user.department.name)
        #     if user.department
        #     else None
        # )

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

    return result


def get_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user if user else None


def update_user(db: Session, user: UserUpdate):
    data = user.model_dump(exclude_unset=True)

    # Clean up foreign keys
    if "departmentId" in data and data["departmentId"] == 0:
        data["departmentId"] = None
    if "managerId" in data and data["managerId"] == 0:
        data["managerId"] = None

    # Fetch existing user
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update core user fields
    for key, value in data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)

    # Update email if provided
    if "email" in data:
        db_cred = (
            db.query(UserCredential).filter(UserCredential.userId == user.id).first()
        )
        if db_cred:
            db_cred.email = data["email"]

    # Update password if provided
    if "password" in data:
        db_cred = (
            db.query(UserCredential).filter(UserCredential.userId == user.id).first()
        )
        if db_cred:
            db_cred.hashedPassword = get_password_hash(data["password"])

    # Update role if provided
    # if "roleId" in data:
    #     # Remove old role entry if exists
    #     db.execute(delete(user_role).where(user_role.c.userId == user.id))
    #     # Insert new role entry
    #     db.execute(insert(user_role).values(userId=user.id, roleId=data["roleId"]))

    db_user.updatedAt = datetime.utcnow()

    db.commit()
    db.refresh(db_user)

    return UserUpdate(
        # id=db_user.id,
        email=db_user.credential.email if db_user.credential else None,
        # roleId=data.get("roleId"),
        **{k: getattr(db_user, k) for k in data if hasattr(db_user, k)},
    )


def toggle_user_activation(user_id: int, activate: bool, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.active = activate
    user.updatedAt = datetime.utcnow()
    db.commit()
    db.refresh(user)

    return {"Message": "User status updated successfully", "status": user.active}
