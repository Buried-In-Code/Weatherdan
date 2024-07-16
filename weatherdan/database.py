__all__ = ["create_db_and_tables", "get_session"]

from sqlmodel import Session, SQLModel, create_engine

from weatherdan.constants import constants
from weatherdan.settings import Source

connect_args = (
    {"check_same_thread": False} if constants.settings.database.source == Source.SQLITE else {}
)
engine = create_engine(constants.settings.database.db_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
