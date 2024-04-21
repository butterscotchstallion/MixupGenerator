from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime

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


"""
meeting
"""


class MeetingBase(BaseModel):
    meeting_timestamp: DateTime
    created_at: DateTime
    updated_at: DateTime


class Meeting(MeetingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    attendees: list[MeetingAttendee]


"""
team
"""


class Team(BaseModel):
    created_at: DateTime
    updated_at: DateTime
