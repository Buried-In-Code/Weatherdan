__all__ = ["Stat"]

from decimal import Decimal

from pydantic import BaseModel


class Stat(BaseModel):
    timestamp: str
    value: Decimal

    def __eq__(self, other):  # noqa: ANN001
        if not isinstance(other, Stat):
            raise NotImplementedError()
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))
