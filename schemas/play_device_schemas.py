from pydantic import BaseModel, PositiveInt


class PlayDeviceBase(BaseModel):
    name: str
    price_per_minute: PositiveInt


class PlayDeviceIn(PlayDeviceBase):
    ...


class PlayDeviceUpdate(PlayDeviceBase):
    name: str | None
    price_per_minute: PositiveInt | None


class PlayDeviceOut(PlayDeviceBase):
    id: int
