from crud.order_crud import get_future_orders_by_device
from crud.play_device_crud import (
    list_all_devices,
    get_device_by_id,
    get_device_by_name,
    insert_device,
    update_device,
    delete_device,
)
from schemas.play_device_schemas import PlayDeviceIn, PlayDeviceUpdate
from utils.exceptions_utils import ObjNotFoundException, ObjUniqueException, ConflictException, NoContentException
from utils.service_base import BaseService


class PlayDeviceService(BaseService):
    async def fetch_all_play_device(self):
        return await list_all_devices(self.db)

    async def get_play_device(self, device_id: int):
        if not (device := await get_device_by_id(self.db, device_id)):
            raise ObjNotFoundException("Play Device", "id", device_id)
        return device

    async def create_play_device(self, device: PlayDeviceIn) -> int:
        if await get_device_by_name(self.db, device.name):
            raise ObjUniqueException("Play Device", "name", device.name)
        device_id = await insert_device(self.db, device)
        await self.db.commit()
        return device_id

    async def update_play_device(self, device_id: int, device: PlayDeviceUpdate):
        await self.get_play_device(device_id)

        if device.name and (place_with_same_name := await get_device_by_name(self.db, device.name)):
            if device_id != place_with_same_name.id:
                raise ObjUniqueException("Play Device", "name", device.name)

        await update_device(self.db, device_id, device)
        await self.db.commit()

    async def delete_play_device(self, device_id: int):
        device = await get_device_by_id(self.db, device_id)
        if not device:
            raise NoContentException

        if len(await get_future_orders_by_device(self.db, device_id)):
            raise ConflictException("there are orders on this play device")

        await delete_device(self.db, device_id)
        await self.db.commit()
