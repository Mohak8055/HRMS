from sqlalchemy.orm import Session, joinedload
from app.models.leave import Leave, LeaveStatus
from app.models.user import User
from app.schemas.leave import LeaveCreate, LeaveUpdate

def create_leave(db: Session, leave: LeaveCreate):
    db_leave = Leave(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def get_leaves_by_user(db: Session, user_id: int):
    return db.query(Leave).filter(Leave.user_id == user_id).all()

def get_all_leaves(db: Session):
    # Use joinedload to fetch the related User object along with the Leave
    return db.query(Leave).options(joinedload(Leave.user)).all()

def update_leave_status(db: Session, leave_id: int, status: LeaveUpdate):
    db_leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if db_leave:
        # Convert string status to Enum member
        db_leave.status = LeaveStatus[status.status.upper()]
        db.commit()
        db.refresh(db_leave)
    return db_leave