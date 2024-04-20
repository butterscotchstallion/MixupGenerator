from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime

"""
meeting_attendee
"""


class MeetingAttendeeBase(BaseModel):
    meeting_id: int
    created_at: DateTime
    updated_at: DateTime
    team_member_id: int


class MeetingAttendee(MeetingAttendeeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MeetingAttendeeCreate(MeetingAttendeeBase):
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
    id: int
    attendees: list[MeetingAttendee]

    class Config:
        orm_mode = True


class MeetingCreate(MeetingBase):
    meeting_timestamp: DateTime


"""
team
"""
