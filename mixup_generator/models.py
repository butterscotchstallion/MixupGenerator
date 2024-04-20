from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from mixup_generator.db import Base


class Meeting(Base):
    """
    Represents a Mixup Meeting between two or more members
    """

    __tablename__ = "meeting"
    id = Column(Integer, primary_key=True)
    meeting_timestamp = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    attendees = relationship("MeetingAttendee", back_populates="attendees")


class MeetingAttendee(Base):
    """
    Each meeting can have a variable number of attendees and they are
    linked to the meeting by the mixup_meeting id
    """

    __tablename__ = "meeting_attendee"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    meeting_id = Column(Integer, ForeignKey("meeting.id"))
    team_member_id = Column(Integer, ForeignKey("team_member.id"))


class TeamMember:
    __tablename__ = "team_member"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    keycloak_user_id = Column(String, unique=True)
    active = Column(Boolean, server_default=expression.false())
    can_attend_multiple_meetings = Column(Boolean, server_default=expression.false())


class Team:
    __tablename__ = "team"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, unique=True)
    active = Column(Boolean, server_default=expression.true())


class TeamMembers:
    """
    Represents team members belonging to one or more team
    """

    __tablename__ = "team_team_member"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    team_member_id = Column(Integer, ForeignKey("team_member.id"))
    team_id = Column(Integer, ForeignKey("team.id"))
