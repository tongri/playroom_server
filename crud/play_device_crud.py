from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.play_device_schemas import PlayDeviceIn, PlayDeviceUpdate
from utils.crud_utils import get_update_set_command


async def list_all_devices(db: AsyncSession):
    return (await db.execute(text("select * from playdevices"))).fetchall()


async def get_device_by_name(db: AsyncSession, name: str):
    return (
        await db.execute(
            text("select * from playdevices where name = :name limit 1"),
            {"name": name}
        )
    ).fetchone()


async def get_device_by_id(db: AsyncSession, device_id: int):
    return (
        await db.execute(
            text("select * from playdevices where id = :id limit 1"),
            {"id": device_id}
        )
    ).fetchone()


async def insert_device(db: AsyncSession, play_device: PlayDeviceIn) -> int:
    res = await db.execute(
        text("insert into playdevices (name, price_per_minute) values (:name, :price_per_minute) returning id"),
        play_device.dict(),
    )
    return res.fetchone()[0]


async def update_device(db: AsyncSession, device_id: int, device: PlayDeviceUpdate):
    set_command = get_update_set_command(device.dict(exclude_unset=True))
    await db.execute(
        text(f"update playdevices set {set_command} where id = :device_id"),
        {**device.dict(exclude_unset=True), "device_id": device_id},
    )


async def delete_device(db: AsyncSession, device_id: int) -> None:
    await db.execute("delete from playdevices where id = :device_id", {"device_id": device_id})
