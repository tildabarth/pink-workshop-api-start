import datetime as dt
import typing as t

from fastapi.encoders import jsonable_encoder
from pydantic.json import ENCODERS_BY_TYPE

from api.schemas import BaseSchema
from settings import get_strftime

# Create custom encoder to use datetime format from settings.
# This enables us to use jsonable_encoder without changing the format
#   of the original datetime data.
# We can override `ENCODERS_BY_TYPE` to make a global change in the
#   `fastapi.encoders.jsonable_encoder`. Better not modify constants though.

def custom_jsonable_encoder(item: BaseSchema) -> t.Any:
    """Convert item to JSON:able, using custom encoder to handle datetime:s."""
    return jsonable_encoder(item, custom_encoder={dt.datetime: get_strftime})
