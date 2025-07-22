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


class UserCredential(Base):
    __tablename__ = "UserCredential"

    id = Column(Integer, primary_key=True)
    userId = Column(
        Integer,
        ForeignKey("User.id", name="fk_user_credential_user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashedPassword = Column(String(255), nullable=False)

    user = relationship("User", back_populates="credential")
    # def __repr__(self):
    #     return f"<UserCredential(id={self.id}, user_id={self.userId}, email={self.email})>"
