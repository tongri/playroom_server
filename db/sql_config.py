from enum import Enum


class FieldTypes(Enum):
    serial = "serial"
    varchar = lambda length: f"varchar({length})"
    boolean = "boolean"
    date = "date"
    smallint = "smallint"
    integer = "integer"
    date_time = "timestamp"


class Constraints(Enum):
    pk = "primary key"
    unique = "unique"
    not_null = "not null"
    unique_not_null = "unique not null"
    check = lambda expr: f"check ({expr})"
    foreign_key = lambda key, parent_table, parent_attr, on_delete: f"foreign key({key}) references {parent_table}" \
                                                                    f"({parent_attr}) on delete {on_delete}"


user_table_name = "MyUsers"
play_devices_table_name = "PlayDevices"
order_table_name = "Orders"


user_table = {
        "name": user_table_name,
        "columns": [
            {
                "name": "id",
                "type": FieldTypes.serial.value,
                "constraints": Constraints.pk.value,
            },
            {
                "name": "password",
                "type": FieldTypes.varchar(256),
                "constraints": Constraints.not_null.value,
            },
            {
                "name": "is_staff",
                "type": FieldTypes.boolean.value,
                "constraints": Constraints.not_null.value,
                "default": "default false"
            },
            {
                "name": "username",
                "type": FieldTypes.varchar(50),
                "constraints": Constraints.check(
                    "char_length(username) >= 4") + " " + Constraints.unique_not_null.value,
            },
        ]
    }

play_devices_table = {
        "name": play_devices_table_name,
        "columns": [
            {
                "name": "id",
                "type": FieldTypes.serial.value,
                "constraints": Constraints.pk.value,
            },
            {
                "name": "name",
                "type": FieldTypes.varchar(128),
                "constraints": Constraints.check("char_length(name) >= 3") + " " + Constraints.unique_not_null.value,
            },
            {
                "name": "price_per_minute",
                "type": FieldTypes.smallint.value,
                "constraints": Constraints.check("price_per_minute > 0") + Constraints.not_null.value,
            },
        ]
    }

order_table = {
        "name": order_table_name,
        "columns": [
            {
                "name": "id",
                "type": FieldTypes.serial.value,
                "constraints": Constraints.pk.value,
            },
            {
                "name": "user_id",
                "type": FieldTypes.integer.value,
            },
            {
                "name": "play_device_id",
                "type": FieldTypes.integer.value,
            },
            {
                "name": "session_time_start",
                "type": FieldTypes.date_time.value,
            },
            {
                "name": "session_time_end",
                "type": FieldTypes.date_time.value,
            },
            {
                "name": "status",
                "type": FieldTypes.varchar(30),
                "constraints": Constraints.not_null.value,
                "default": "default 'pending'"
            },
            {
                "name": "players",
                "type": FieldTypes.smallint.value,
                "constraints": Constraints.check("players >= 0")
            },
            {
                "name": Constraints.foreign_key("user_id", user_table_name, "id", "cascade")
            },
            {
                "name": Constraints.foreign_key("play_device_id", play_devices_table_name, "id", "cascade")
            }
        ],
    }


all_tables = [
    user_table, play_devices_table, order_table,
]
