import datetime as dt
import typing as t

from pydantic import BaseModel


class RunCreate(BaseModel):
    """Schema with required properties when creating a run item."""
    ...


class Run(RunCreate):
    """Schema with required properties when reading a run item."""
    ...
