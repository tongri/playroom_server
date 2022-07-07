from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from schemas.order_schemas import OrderOut, OrderIn, OrderOutAdmin
from schemas.user_schemas import UserOut
from services.order_service import OrderService, OrderStatuses
from dependencies import get_admin, async_get_db, get_current_user
from starlette import status

from utils.pagination_utils import PaginationParams, from_response_to_page

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=Page[OrderOut])
async def get_orders(
    page: PaginationParams = Depends(PaginationParams),
    db: AsyncSession = Depends(async_get_db),
    user: UserOut = Depends(get_current_user),
):
    return from_response_to_page(page, await OrderService(db).fetch_user_orders(user.id))


@router.get("/admin/", response_model=Page[OrderOutAdmin])
async def get_admin_orders(
    page: PaginationParams = Depends(PaginationParams),
    db: AsyncSession = Depends(async_get_db),
    _=Depends(get_admin),
):
    return from_response_to_page(page, await OrderService(db).admin_fetch_orders())


@router.post("/{play_device_id}/", response_model=OrderOut)
async def create_order(
    play_device_id: int,
    order: OrderIn,
    db: AsyncSession = Depends(async_get_db),
    user: UserOut = Depends(get_current_user),
):
    return await OrderService(db).create_order(play_device_id, user.id, order)


@router.delete("/{order_id}/", status_code=status.HTTP_200_OK)
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(async_get_db),
    user: UserOut = Depends(get_current_user),
):
    await OrderService(db).delete_user_order(order_id, user.id)


@router.patch("/{order_id}/", response_model=OrderOutAdmin)
async def update_status(
    order_id: int,
    new_status: OrderStatuses,
    db: AsyncSession = Depends(async_get_db),
    _=Depends(get_admin),
):
    return await OrderService(db).update_order(order_id, new_status.value)


@router.get("/statistics/")
async def get_statistics(db: AsyncSession = Depends(async_get_db)):
    return await OrderService(db).get_statistics_by_device()
