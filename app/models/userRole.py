from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base


user_role = Table(
    "UserRole",
    Base.metadata,
    Column(
        "userId", Integer, ForeignKey("User.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "roleId", Integer, ForeignKey("Role.id", ondelete="CASCADE"), primary_key=True
    ),
)
