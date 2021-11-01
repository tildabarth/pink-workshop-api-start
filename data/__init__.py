"""Save data from Strava API to JSON files.

This operation corresponds to populating a database.
It only has to be run once. However, if the schema keys change names, they may
    need to be updated in the item's save function.
"""
import json
import logging
import typing as t
from pathlib import Path

from api.schemas import runs as run_schemas, shoes as shoe_schemas


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

ItemDict = t.Dict[str, t.Any]
ItemCollection = t.List[ItemDict]
ItemCollectionDict = t.Dict[int, ItemDict]

INDENT: int = 2
ENCODING: str = 'utf-8'

DATA_DIR = Path(__file__).parent
API_SOURCE = DATA_DIR / 'strava_api'
TARGET_DIR = DATA_DIR / 'db'
BACKUP_DIR = DATA_DIR / 'backups'

RUNS_SOURCE = API_SOURCE / 'runs.json'
RUNS_TARGET = TARGET_DIR / 'runs.json'
RUNS_BACKUP_TARGET = BACKUP_DIR / 'runs.json'

SHOES_SOURCE = API_SOURCE / 'shoes.json'
SHOES_TARGET = TARGET_DIR / 'shoes.json'
SHOES_BACKUP_TARGET = BACKUP_DIR / 'shoes.json'

# Map keys in original data to schema keys.
SHOE_KEYS_TO_REPLACE = {}
RUN_KEYS_TO_REPLACE = {
    'moving_time': 'duration',
    'start_date': 'start',
    'gear_id': 'shoe_id',
    'average_speed': 'speed',
    'average_heartrate': 'heart_rate',
}


def main(override: bool = True):
    # Create target directory
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    shoe_ids = save_shoes(override_target=override)
    save_runs(shoe_ids, override_target=override)


def save_shoes(override_target: bool = False, backup: bool = True) -> t.Optional[t.Dict[str, int]]:
    """Store shoes as dicts based on Pydantic schema."""
    try:
        with SHOES_TARGET.open('r', encoding=ENCODING) as f:
            if override_target is False:
                # Prevent overriding existing target file.
                logger.debug(f'Target file already exists: {SHOES_TARGET}')
                return None
    except FileNotFoundError:
        # Continue running code to create target file and save data.
        pass
    with SHOES_SOURCE.open('r', encoding=ENCODING) as f:
        shoe_collection: ItemCollection = json.load(f)

    shoe_ids = {}
    schema_collection: ItemCollectionDict = {}
    for item_id, shoe_dict in enumerate(shoe_collection, start=1):
        # Store old id to enable converting in runs.
        shoe_ids[shoe_dict['id']] = item_id
        for dict_key, schema_key in SHOE_KEYS_TO_REPLACE.items():
            # Replace dict key with schema key.
            if dict_key in shoe_dict:
                shoe_dict[schema_key] = shoe_dict[dict_key]
                del shoe_dict[dict_key]
        shoe_dict_create: ItemDict = shoe_schemas.ShoeCreate(**shoe_dict).dict()
        shoe_dict_read: ItemDict = shoe_schemas.Shoe(id=item_id, **shoe_dict_create).dict()
        schema_collection[item_id] = shoe_dict_read

    # Store new collection in target file.
    with SHOES_TARGET.open('w', encoding=ENCODING) as f:
        json.dump(schema_collection, f, indent=INDENT)
    logger.info(f'Saved shoe data to {SHOES_TARGET}')

    if backup:
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        with SHOES_BACKUP_TARGET.open('w', encoding=ENCODING) as f:
            json.dump(schema_collection, f, indent=INDENT)
        logger.info(f'Backed up shoe data to {SHOES_BACKUP_TARGET}')
    return shoe_ids


def save_runs(shoe_ids: t.Dict[str, id], override_target: bool = False, backup: bool = True):
    """Store runs as dicts based on Pydantic schema."""
    try:
        with RUNS_TARGET.open('r', encoding=ENCODING) as f:
            if override_target is False:
                # Prevent overriding existing target file.
                logger.debug(f'Target file already exists: {RUNS_TARGET}')
                return None
    except FileNotFoundError:
        # Continue running code to create target file and save data.
        pass
    with RUNS_SOURCE.open('r', encoding=ENCODING) as f:
        run_collection: ItemCollection = json.load(f)

    schema_collection: ItemCollection = {}
    for item_id, run_dict in enumerate(run_collection, start=1):
        for dict_key, schema_key in RUN_KEYS_TO_REPLACE.items():
            # Replace dict key with schema key.
            if dict_key in run_dict:
                run_dict[schema_key] = run_dict[dict_key]
                if schema_key == 'shoe_id':
                    run_dict[schema_key] = shoe_ids.get(run_dict[dict_key])
                del run_dict[dict_key]

        run_dict_create: ItemDict = run_schemas.RunCreate(**run_dict).dict()
        run_dict_read: ItemDict = run_schemas.Run(id=item_id, **run_dict_create).dict()
        # Convert start time back to string to enable serializing.
        if 'start' in run_dict_read:
            run_dict_read['start'] = run_dict['start']
        schema_collection[item_id] = run_dict_read

    # Store new collection in target file.
    with RUNS_TARGET.open('w', encoding=ENCODING) as f:
        json.dump(schema_collection, f, indent=INDENT)
    logger.info(f'Saved run data to {RUNS_TARGET}')

    if backup:
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        with RUNS_BACKUP_TARGET.open('w', encoding=ENCODING) as f:
            json.dump(schema_collection, f, indent=INDENT)
        logger.info(f'Backed up run data to {RUNS_BACKUP_TARGET}')


if __name__ == '__main__':
    main()
