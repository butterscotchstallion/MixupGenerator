from pydantic import BaseModel
from sqlalchemy import DateTime


class MeetingBase(BaseModel):
    meeting_timestamp: DateTime
    created_at: DateTime
    updated_at: DateTime


class Meeting(MeetingBase):
    id: int

    class Config:
        orm_mode = True


class MeetingCreate(MeetingBase):
    meeting_timestamp: DateTime
