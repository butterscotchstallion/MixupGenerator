from sqlalchemy.orm import Session

from mixup_generator import schemas

from . import models


def get_meeting(db: Session, meeting_id: int):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()


def create_meeting(db: Session, meeting: schemas.MeetingCreate) -> models.Meeting:
    """
    TODO figure out attendees
    """
    db_meeting = models.Meeting(meeting_timestamp=meeting.meeting_timestamp)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def add_attendee(db: Session, meeting_attendee: schemas.Meeting):
    pass
