import json
import typing as t
from pathlib import Path


class CommitError(ValueError):
    """Raise when commit failed."""
    ...


class ItemExistsError(ValueError):
    """Raise when item exists."""
    ...


class ItemNotFoundError(ValueError):
    """Raise when item does not exist."""
    ...


ItemDict = t.Dict[str, t.Any]
ItemCollection = t.Dict[str, ItemDict]

ENCODING: str = 'utf-8'


def item_id_existst(item_id: int, collection: ItemCollection) -> bool:
    """Check if item id existst in collection."""
    return str(item_id) in collection


def get_collection_dict(source: Path)-> ItemCollection:
    """Get collection data from JSON source."""
    with source.open('r', encoding=ENCODING) as f:
        return json.load(f)


def get_item_dict(item_id: int, source: Path) -> t.Optional[ItemDict]:
    """Get item by id."""
    collection = get_collection_dict(source)
    return collection.get(str(item_id))


def commit_changes(collection: ItemCollection, source: Path) -> None:
    """Save changes to collection."""
    try:
        with source.open('w', encoding=ENCODING) as f:
            json.dump(collection, f, indent=2)
    except json.JSONDecodeError:
        raise CommitError(f'Cannot commit data to {source}')


def create_item_dict(item_dict: ItemDict, source: Path) -> ItemDict:
    """Create item in collection."""
    collection = get_collection_dict(source)
    if (item_id := item_dict.get('id')) and item_id_existst(item_id, collection):
        raise ItemExistsError('Cannot add item, id existst')
    if item_id is None:
        # Generate new id
        item_id = max(int(key) for key in collection.keys()) + 1
    item_dict['id'] = item_id
    collection[str(item_id)] = item_dict
    commit_changes(collection, source)
    return item_dict


def update_item_dict(item_id, item_dict: ItemDict, source: Path) -> ItemDict:
    """Update item in collection."""
    collection = get_collection_dict(source)
    if not item_id_existst(item_id, collection):
        raise ItemNotFoundError('Cannot update non-existing item')
    item_dict['id'] = item_id  # Make sure item has correct id
    updated_dict = collection[str(item_id)]
    updated_dict.update(item_dict)
    commit_changes(collection, source)
    return updated_dict


def delete_item_dict(item_id: int, source: Path) -> None:
    """Delete item from collection."""
    collection = get_collection_dict(source)
    if item_id_existst(item_id, collection):
        del collection[str(item_id)]
        commit_changes(collection, source)
    return None
