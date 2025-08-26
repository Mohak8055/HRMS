from sqlalchemy import (
    Column,
    Integer,
    Date,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.userRole import user_role  # Import AFTER it is defined
from app.models.role import Role
from app.models.userprofile import ProfilePhoto


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True)
    firstName = Column(String(100))
    lastName = Column(String(100))
    dob = Column(Date, nullable=False)
    doj = Column(Date, nullable=False)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    active = Column(Boolean, default=True, nullable=False)  # Active flag
    departmentId = Column(
        Integer, ForeignKey("Department.id", name="fk_department_id"), nullable=True
    )
    # Self-referential relationship for hierarchy
    managerId = Column(
        Integer, ForeignKey("User.id", name="fk_user_manager_id"), nullable=True
    )
    # Relationships
    department = relationship("Department", back_populates="users")
    manager = relationship("User", remote_side=[id], back_populates="subordinates")
    subordinates = relationship("User", back_populates="manager", cascade="all, delete")

    credential = relationship("UserCredential", back_populates="user", uselist=False)
    roles = relationship("Role", secondary=user_role, backref="users")
    profile_photo = relationship("ProfilePhoto", back_populates="user", uselist=False)

