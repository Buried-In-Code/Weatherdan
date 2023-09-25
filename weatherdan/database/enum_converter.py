__all__ = ["EnumConverter"]

from enum import Enum
from typing import Self

from pony.orm.dbapiprovider import StrConverter


class EnumConverter(StrConverter):
    def validate(self: Self, val, obj=None) -> Enum:  # noqa: ANN001, ARG002
        if not isinstance(val, Enum):
            msg = f"Must be an Enum. Got {type(val)}"
            raise TypeError(msg)
        return val

    def py2sql(self: Self, val: Enum) -> str:
        return val.name

    def sql2py(self: Self, value: str) -> Enum:
        return self.py_type[value]
