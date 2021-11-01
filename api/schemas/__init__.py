from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Custom base schema."""

    class Config:
        allow_mutation = True
        anystr_strip_whitespace = True
        use_enum_values = True
        validate_assignment = True
