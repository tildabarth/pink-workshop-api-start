import typing as t

from api.schemas import shoes as shoe_schemas


async def index():
    """Get all items."""
    return []


async def get(item_id: int):
    """Get item by id."""
    return {}


async def create(item: shoe_schemas.ShoeCreate):
    """Create new item."""
    return {}


async def update(item_id: int, item: shoe_schemas.ShoeCreate):
    """Update item by id."""
    return {}


async def deletete(item_id: int):
    """Delete item by id."""
    return None
