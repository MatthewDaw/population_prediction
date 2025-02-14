"""Common functions for population data analysis."""

import json

from pydantic import BaseModel, ConfigDict


class BasePydanticForRepo(BaseModel):
    """Base Pydantic class for the repo."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __hash__(self):
        """Convert Pydantic model to a hashable format."""
        return hash(json.dumps(self.model_dump(), sort_keys=True))


def deduplicate_list(input_list):
    """Deduplicate a list."""
    seen = set()
    deduplicated_values = [
        x for x in input_list if not (str(x) in seen or seen.add(str(x)))
    ]
    return deduplicated_values
