from datetime import datetime

from pydantic import BaseModel, PositiveInt, validator, root_validator

from schemas.play_device_schemas import PlayDeviceOut
from schemas.user_schemas import UserPublic


class OrderBase(BaseModel):
    session_time_start: datetime
    session_time_end: datetime
    players: int

    @validator("session_time_end", "session_time_start")
    def validate_show_time_start_future(cls, v):
        if not v.astimezone() > datetime.now().astimezone():
            raise ValueError("Order can't be held in past")
        return v

    @root_validator
    def check_session_times(cls, values):
        start, end = values.get('session_time_start'), values.get('session_time_end')
        if all([start, end]) and start >= end:
            raise ValueError('Session beginning must be before end')
        return values


class OrderIn(OrderBase):
    ...


class OrderOut(OrderBase):
    id: int
    play_device: PlayDeviceOut
    status: str


class OrderOutAdmin(OrderBase):
    id: int
    play_device: PlayDeviceOut
    user: UserPublic
    status: str
