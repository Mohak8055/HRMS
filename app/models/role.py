from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.database import Base  # or your Base import


class Role(Base):
    __tablename__ = "Role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    alias = Column(String(100), nullable=False)
    active = Column(Boolean, default=True, nullable=False)  # Active flag
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
