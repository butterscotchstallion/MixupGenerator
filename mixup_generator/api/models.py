from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlmodel import Field, SQLModel


class TeamTeamMembersLink(SQLModel, table=True):
    team_member_id: int | None = Field(
        default=None, foreign_key="teammember.id", primary_key=True
    )
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )


class TeamMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    name: str = Field(String, unique=True, max_length=50)
    keycloak_user_id: str = Field(String, max_length=10, unique=True)
    active: bool = Field(sa_column=Column(Boolean), default=True)
    can_attend_multiple_meetings: bool = Field(sa_column=Column(Boolean), default=True)
    """
    teams: list[Team] = Relationship(
        back_populates="teammembers", link_model=TeamTeamMembersLink
    )
    """


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    name: str = Field(String, unique=True, max_length=50)
    active: bool = Field(sa_column=Column(Boolean), default=True)
    """
    members: list[TeamMember] = Relationship(
        back_populates="teams", link_model=TeamTeamMembersLink
    )
    """


class MeetingLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    name: str = Field(String, unique=True, max_length=50)


class Meeting(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meeting_timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )

    # meeting_attendees: list[TeamMember] = Relationship(back_populates="meeting")
    meeting_location_id: int = Field(foreign_key="meetinglocation.id")


class MeetingAttendee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        ),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now(), nullable=True),
    )
    meeting_id: int = Field(foreign_key="meeting.id")
    team_member_id: int = Field(foreign_key="teammember.id")
    # Links to meeting_attendees
    # meeting: Meeting = Relationship(back_populates="meeting_attendees")
