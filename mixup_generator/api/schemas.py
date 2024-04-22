from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime

"""
team
"""


class Team(BaseModel):
    id: int
    created_at: DateTime
    updated_at: DateTime
    name: str


class TeamMember(BaseModel):
    id: int
    name: str
    created_at: DateTime
    updated_at: DateTime


"""
meeting
"""


class Meeting(BaseModel):
    id: int
    meeting_timestamp: DateTime
    created_at: DateTime
    updated_at: DateTime
    attendees: list[TeamMember]


"""
meeting_attendee
"""


class MeetingAttendee(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: DateTime
    updated_at: DateTime
    meeting_id: int
    team_member_id: int
