from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from mixup_generator.db import Base


class Meetings(Base):
    """
    Represents a Mixup Meeting between two or more members

    meetings
    ===================
    id
    meeting_timestamp
    created_at
    updated_at

    meeting_attendees
    ===================
    id
    member
    created_at
    updated_at
    """

    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True)
    meeting_timestamp = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    attendees = relationship("MeetingAttendees", back_populates="attendees")


class MeetingAttendees(Base):
    """
    Each meeting can have a variable number of attendees and they are
    linked to the meeting by the mixup_meeting id
    """

    __tablename__ = "meeting_attendees"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
