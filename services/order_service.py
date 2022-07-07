from enum import Enum

from crud.order_crud import (
    get_user_orders,
    get_orders,
    insert_order,
    get_order_by_id,
    delete_order, get_order_by_id_short, update_order_status, get_order_by_id_admin, get_device_statistics,
)
from crud.play_device_crud import get_device_by_id
from schemas.order_schemas import OrderIn
from utils.exceptions_utils import ObjNotFoundException, NoContentException, ConflictException
from utils.service_base import BaseService


class OrderStatuses(Enum):
    accepted = "accepted"
    declined = "declined"


class OrderService(BaseService):
    async def fetch_user_orders(self, user_id: int):
        return await get_user_orders(self.db, user_id)

    async def admin_fetch_orders(self):
        return await get_orders(self.db)

    async def create_order(self, play_device_id: int, user_id: int, order: OrderIn):

        if not await get_device_by_id(self.db, play_device_id):
            raise ObjNotFoundException("Play device", "id", play_device_id)

        record_id = await insert_order(self.db, play_device_id, user_id, order)
        await self.db.commit()
        return await get_order_by_id(self.db, record_id)

    async def delete_user_order(self, order_id: int, user_id: int):
        order_to_delete = await get_order_by_id_short(self.db, order_id)

        if not order_to_delete:
            raise NoContentException

        if order_to_delete.user_id != user_id:
            raise ObjNotFoundException("Order", "id", order_id)

        await delete_order(self.db, order_id)
        await self.db.commit()

    async def update_order(self, order_id: int, new_status: str):
        order_to_update = await get_order_by_id_short(self.db, order_id)

        if order_to_update.status == new_status:
            raise ConflictException(f"Order already has status {new_status}")

        await update_order_status(self.db, order_id, new_status)
        await self.db.commit()
        return await get_order_by_id_admin(self.db, order_id)

    async def get_statistics_by_device(self):
        return await get_device_statistics(self.db)
