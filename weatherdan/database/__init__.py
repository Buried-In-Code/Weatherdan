__all__ = ["DATABASE_PATH"]

from enum import Enum

from weatherdan import get_data_root
from weatherdan.database.enum_converter import EnumConverter
from weatherdan.database.tables import db

DATABASE_PATH = get_data_root() / "weatherdan.sqlite"
db.bind(
    provider="sqlite",
    filename=str(DATABASE_PATH),
    create_db=True,
)
db.provider.converter_classes.append((Enum, EnumConverter))
db.generate_mapping(create_tables=True)


@db.on_connect(provider="sqlite")
def sqlite_case_sensitivity(database, connection) -> None:  # noqa: ARG001, ANN001
    cursor = connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = OFF")
