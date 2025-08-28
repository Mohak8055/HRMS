from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.database import get_db
from app.models.user import User
from app.models.userCredential import UserCredential
from app.utils.auth import verify_password, create_tokens

router = APIRouter()

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user_cred = (
        db.query(UserCredential)
        .options(
            joinedload(UserCredential.user).joinedload(User.roles)
        )
        .filter(UserCredential.email == form_data.username) # Use form_data.username
        .first()
    )

    if not user_cred or not verify_password(form_data.password, user_cred.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token payload
    token_data = {
        "email": user_cred.email,
        "userId": user_cred.userId,
        "roles": [{"roleId": role.id, "name": role.name} for role in user_cred.user.roles],
    }
    
    tokens = create_tokens(data=token_data)

    # Return a rich response for the frontend to store
    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
        "refresh_token": tokens["refresh_token"],
        "firstName": user_cred.user.firstName,
        "lastName": user_cred.user.lastName,
        "email": user_cred.email,
        "userId": user_cred.userId,
        "roles": [{"roleId": role.id, "name": role.name} for role in user_cred.user.roles],
        "phone": user_cred.user.phone,
        "departmentId": user_cred.user.departmentId,
        "managerId": user_cred.user.managerId,
        "active": user_cred.user.active,
    }