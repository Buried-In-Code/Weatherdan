__all__ = ["User"]

from pydantic import BaseModel


class User(BaseModel):
    username: str

    def __lt__(self, other):
        if not isinstance(other, User):
            raise NotImplementedError()
        return self.username < other.username
