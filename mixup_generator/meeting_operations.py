from sqlalchemy.orm import Session

from mixup_generator import schemas

from . import models


def get_meeting(db: Session, meeting_id: int):
    """
    TODO figure out attendees
    """
    return db.query(models.Meetings).filter(models.Meetings.id == meeting_id).first()


def create_meeting(db: Session, meeting: schemas.MeetingCreate):
    db_meeting = models.Meetings(meeting_timestamp=meeting.meeting_timestamp)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting
