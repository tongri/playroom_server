from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from schemas.play_device_schemas import PlayDeviceIn, PlayDeviceUpdate, PlayDeviceOut
from services.play_device_service import PlayDeviceService
from dependencies import get_admin, async_get_db
from starlette import status

from utils.pagination_utils import PaginationParams, from_response_to_page

router = APIRouter(prefix="/play_devices", tags=["play_devices"])


@router.get("/", response_model=Page[PlayDeviceOut])
async def read_devices(
    page: PaginationParams = Depends(PaginationParams), db: AsyncSession = Depends(async_get_db)
):
    return from_response_to_page(
        page, await PlayDeviceService(db).fetch_all_play_device()
    )


@router.get("/{play_device_id}/", response_model=PlayDeviceOut)
async def retrieve_device(play_device_id: int, db: AsyncSession = Depends(async_get_db)):
    return await PlayDeviceService(db).get_play_device(play_device_id)


@router.post("/", response_model=PlayDeviceOut)
async def create_device(
    play_device: PlayDeviceIn,
    _=Depends(get_admin),
    db: AsyncSession = Depends(async_get_db),
):
    last_record_id = await PlayDeviceService(db).create_play_device(play_device)
    return {**play_device.dict(), "id": last_record_id}


@router.patch("/{play_device_id}/", response_model=PlayDeviceOut)
async def patch_device(
    play_device_id: int,
    play_device: PlayDeviceUpdate,
    _=Depends(get_admin),
    db: AsyncSession = Depends(async_get_db),
):
    service = PlayDeviceService(db)
    await service.update_play_device(play_device_id, play_device)
    return await service.get_play_device(play_device_id)


@router.delete("/{play_device_id}/", status_code=status.HTTP_200_OK)
async def remove_device(
    play_device_id: int, _=Depends(get_admin), db: AsyncSession = Depends(async_get_db)
):
    await PlayDeviceService(db).delete_play_device(play_device_id)
