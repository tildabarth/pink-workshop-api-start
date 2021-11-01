import typing as t
from enum import Enum

from pydantic import BaseModel


class Color(Enum):
    """Shoe colour."""

    black: str = 'black'
    blue: str = 'blue'
    green: str = 'green'
    mixed: str = 'mixed'
    orange: str = 'orange'
    pink: str = 'pink'
    purple: str = 'purple'
    red: str = 'red'
    white: str = 'white'
    yellow: str = 'yellow'


class ShoeCreate(BaseModel):
    """Schema with required properties when creating a shoe item."""
    ...


class Shoe(ShoeCreate):
    """Schema with required properties when reading a shoe item."""
    ...
