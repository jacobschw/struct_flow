from typing import Any


class ParsedFile:

    def __init__(self, parsed_structure: dict[str, list[str]]):
        self._store = parsed_structure

    def __str__(self) -> str:
        """String representation of the class."""
        return str(self._store)

    def __repr__(self) -> str:
        """Representation of an enum instance."""
        return self._store.__repr__()

    def extract_fields(self, *fields: str):
        pass
