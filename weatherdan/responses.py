__all__ = ["ErrorResponse"]

from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    timestamp: datetime
    status: str
    reason: str
