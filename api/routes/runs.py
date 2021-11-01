import typing as t

from api.schemas import runs as run_schemas


async def index():
    """Get all items."""
    return []


async def get(item_id: int):
    """Get item by id."""
    return {}


async def create(item: run_schemas.RunCreate):
    """Create new item."""
    return {}


async def update(item_id: int, item: run_schemas.Run):
    """Update item by id."""
    return {}


async def delete(item_id: int):
    """Delete item by id."""
    return None
