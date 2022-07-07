from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from schemas.order_schemas import OrderIn
from utils.crud_utils import accumulated_dict_fetch_all, accumulated_dict_fetch_one

ORDER_SELECT = "select o.id id, status, session_time_start, session_time_end, " \
               "players, name as play_device__name, price_per_minute play_device__price_per_minute, " \
               " pl.id as play_device__id from orders o inner join playdevices pl on " \
               "pl.id = o.play_device_id"


ORDER_SELECT_ADMIN = "select o.id id, status, session_time_start, session_time_end, " \
               "players, name as play_device__name, price_per_minute play_device__price_per_minute, " \
               " pl.id as play_device__id, u.id user__id, u.username user__username " \
               "from orders o inner join playdevices pl on pl.id = o.play_device_id " \
                     "inner join myusers u on u.id = o.user_id"


ORDERS_BY_DEVICES = "select p.id id, count(*) total_orders, p.name device_name, p.price_per_minute price_per_minute, " \
                  "string_agg(u.username, ', ') users_ordered from orders o join playdevices p " \
                  "on o.play_device_id = p.id left join myusers u on o.user_id = u.id " \
                  "where o.status = 'accepted' group by p.id order by total_orders desc;"


async def get_future_orders_by_device(db: AsyncSession, device_id: int):
    res = await db.execute(
        text("select * from orders where play_device_id = :device_id and "
             "session_time_end > now() and status = 'accepted'"),
        {"device_id": device_id}
    )
    return res.fetchall()


async def get_user_orders(db: AsyncSession, user_id: int):
    res = await db.execute(
            text(f"{ORDER_SELECT} where user_id = :user_id"),
            {"user_id": user_id}
        )
    return accumulated_dict_fetch_all(res.cursor)


async def get_orders(db: AsyncSession):
    res = await db.execute(text(f"{ORDER_SELECT_ADMIN}"))
    return accumulated_dict_fetch_all(res.cursor)


async def get_order_by_id(db: AsyncSession, order_id: int):
    res = await db.execute(
            text(f"{ORDER_SELECT} where o.id = :order_id limit 1"),
            {"order_id": order_id}
        )
    return accumulated_dict_fetch_one(res.cursor)


async def get_order_by_id_admin(db: AsyncSession, order_id: int):
    res = await db.execute(
            text(f"{ORDER_SELECT_ADMIN} where o.id = :order_id limit 1"),
            {"order_id": order_id}
        )
    return accumulated_dict_fetch_one(res.cursor)


async def get_user_order_by_id(db: AsyncSession, order_id: int, user_id: int):
    return (
        await db.execute(
            text(f"{ORDER_SELECT} where order_id = :order_id and user_id = :user_id limit 1"),
            {"order_id": order_id, "user_id": user_id}
        )
    ).fetchone()


async def get_order_by_id_short(db: AsyncSession, order_id: int):
    return (
        await db.execute(
            text(f"select * from orders where id = :order_id limit 1"),
            {"order_id": order_id}
        )
    ).fetchone()


async def insert_order(db: AsyncSession, play_device_id: int, user_id, order: OrderIn):
    res = await db.execute(
        text("insert into orders (user_id, play_device_id, session_time_start,"
             " session_time_end, players) values (:user_id, :play_device_id, "
             ":session_time_start, :session_time_end, :players) returning id"),
        {"user_id": user_id, "play_device_id": play_device_id, **order.dict()}
    )
    return res.fetchone()[0]


async def update_order_status(db: AsyncSession, order_id: int, new_status: str):
    await db.execute(
        text("update orders set status = :new_status where id = :order_id"),
        {"new_status": new_status, "order_id": order_id}
    )


async def delete_order(db: AsyncSession, order_id: int):
    await db.execute(
        text("delete from orders where id = :order_id"),
        {"order_id": order_id}
    )


async def get_device_statistics(db: AsyncSession):
    res = accumulated_dict_fetch_all((await db.execute(ORDERS_BY_DEVICES)).cursor)

    for entry in res:
        entry["users_ordered"] = entry["users_ordered"].split(", ")

    return res

