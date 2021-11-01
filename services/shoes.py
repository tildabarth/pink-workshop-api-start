import typing as t

from settings import get_settings
from data import SHOES_TARGET as SHOES_SOURCE
from services import (
    create_item_dict,
    delete_item_dict,
    get_collection_dict,
    get_item_dict,
    update_item_dict
)

ItemDict = t.Dict[str, t.Any]
ItemCollection = t.Dict[str, ItemDict]

settings = get_settings()


def get_collection() -> ItemCollection:
    """Get shoes from JSON source."""
    return get_collection_dict(SHOES_SOURCE)


def get_dicts() -> t.List[ItemDict]:
    """Return item dicts sorted on distance in descending order."""
    collection = get_collection()
    return sorted(
        collection.values(),
        key=lambda item: (item['distance'], item['brand'], item['model']),
        reverse=True,
    )


def get_dict(item_id: int) -> t.Optional[ItemDict]:
    """Get shoe by id."""
    return get_item_dict(item_id, SHOES_SOURCE)


def create_dict(item_dict: ItemDict) -> ItemDict:
    """Create shoe in collection."""
    return create_item_dict(item_dict, SHOES_SOURCE)


def update_dict(item_id: int, item_dict: ItemDict) -> ItemDict:
    """Update shoe in collection."""
    return update_item_dict(item_id, item_dict, SHOES_SOURCE)


def delete_dict(item_id: int) -> None:
    """Delete shoe from collection."""
    return delete_item_dict(item_id, SHOES_SOURCE)
