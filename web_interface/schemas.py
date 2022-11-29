__all__ = ["Device", "Stat"]

from decimal import Decimal

from pydantic import BaseModel, Field


class Stat(BaseModel):
    timestamp: str
    value: Decimal

    def __eq__(self, other):
        if not isinstance(other, Stat):
            raise NotImplementedError()
        return self.timestamp == other.timestamp

    def __hash__(self):
        return hash((type(self), self.timestamp))


class Device(BaseModel):
    name: str
    stats: list[Stat] = Field(default_factory=list)

    def __lt__(self, other):
        if not isinstance(other, Device):
            raise NotImplementedError()
        return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, Device):
            raise NotImplementedError()
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))
