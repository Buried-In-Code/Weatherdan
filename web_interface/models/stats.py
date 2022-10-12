__all__ = ["Stats"]

from pydantic import BaseModel, Field


class Stats(BaseModel):
    daily: dict[str, str] = Field(default_factory=dict)
    weekly: dict[str, str] = Field(default_factory=dict)
    monthly: dict[str, str] = Field(default_factory=dict)
    yearly: dict[str, str] = Field(default_factory=dict)
