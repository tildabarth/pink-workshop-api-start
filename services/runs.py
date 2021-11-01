import datetime as dt
import typing as t

from settings import get_settings
from data import RUNS_TARGET as RUNS_SOURCE
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


def datetime_to_string(item_datetime: t.Optional[dt.datetime]) -> t.Optional[str]:
    """Convert datetime to string.

    Any datetime must be converted to string before serializing.
    """
    if item_datetime:
        return item_datetime.strftime(settings.datetime_format)


def string_to_datetime(item_datetime: dt.datetime) -> str:
    """Convert string to datetime."""
    return dt.datetime.strptime(item_datetime, settings.datetime_format)


def get_collection() -> ItemCollection:
    """Get runs from JSON source."""
    return get_collection_dict(RUNS_SOURCE)


def get_dicts() -> t.List[ItemDict]:
    """Return item dicts sorted on start time in descending order."""
    collection = get_collection()
    return sorted(
        collection.values(),
        key=lambda item: string_to_datetime(item['start']), reverse=True)


def get_dict(item_id: int) -> t.Optional[ItemDict]:
    """Get run by id."""
    return get_item_dict(item_id, RUNS_SOURCE)


def create_dict(item_dict: ItemDict) -> ItemDict:
    """Create run in collection."""
    if 'start' in item_dict:
        item_dict['start'] = datetime_to_string(item_dict['start'])
    return create_item_dict(item_dict, RUNS_SOURCE)


def update_dict(item_id: int, item_dict: ItemDict) -> ItemDict:
    """Update run in collection."""
    if 'start' in item_dict:
        item_dict['start'] = datetime_to_string(item_dict['start'])
    return update_item_dict(item_id, item_dict, RUNS_SOURCE)


def delete_dict(item_id: int) -> None:
    """Delete run from collection."""
    return delete_item_dict(item_id, RUNS_SOURCE)
