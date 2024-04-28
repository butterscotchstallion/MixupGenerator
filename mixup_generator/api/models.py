from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String
from sqlmodel import TIMESTAMP, Field, Relationship, SQLModel, text


class TeamMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    name: str = Field(String, unique=True, max_length=50)
    keycloak_user_id: str = Field(String, max_length=10, unique=True)
    active: bool = Field(sa_column=Column(Boolean), default=True)
    can_attend_multiple_meetings: bool = Field(sa_column=Column(Boolean), default=True)


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    name: str = Field(String, unique=True, max_length=50)
    active: bool = Field(sa_column=Column(Boolean), default=True)


class Meeting(SQLModel, table=True):
    """
    Represents a Mixup Meeting between two or more members
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    meeting_timestamp: DateTime = Field(DateTime(timezone=True))
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )

    attendees: list[TeamMember] = Relationship(back_populates="team")
    meeting_location_id: int = Field(foreign_key="meeting_location._id")


class MeetingLocation(SQLModel, table=True):
    """
    Represents a meeting room
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    name: str = Field(String, unique=True, max_length=50)


class MeetingAttendee(SQLModel, table=True):
    """
    Each meeting can have a variable number of attendees and they are
    linked to the meeting by the mixup_meeting id
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    meeting_id: int = Field(foreign_key="meeting.id")
    team_member_id: int = Field(foreign_key="team_member.id")


class TeamTeamMembers(SQLModel, table=True):
    """
    Represents team members belonging to one or more team
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    team_member_id: int = Field(foreign_key="team_member.id")
    team_id: int = Field(foreign_key="team.id")
