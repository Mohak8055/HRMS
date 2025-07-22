from sqlalchemy.orm import Session
from app.models.user import User
from app.models.userCredential import UserCredential
from app.schemas.user import UserCreate
from app.utils.auth import get_password_hash


def user_login(db: Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password", "email"}))
    data = user.model_dump()
    # Clean up foreign keys: convert 0 to None
    if data.get("departmentId") == 0:
        data["departmentId"] = None
    if data.get("managerId") == 0:
        data["managerId"] = None
    # Extract and remove email and password from user payload
    email = data.pop("email")
    plain_password = data.pop("password")
    hashPassword = get_password_hash(plain_password)
    db_user = User(**data)
    db.add(db_user)  # Add the user to the session
    db.flush()  # Ensure the user is added to the session before committing
    print(hashPassword)
    credentail = UserCredential(
        userId=db_user.id, email=email, hashedPassword=hashPassword
    )
    db.add(credentail)
    db.commit()
    db.refresh(db_user)
    return db_user
