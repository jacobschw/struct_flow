import csv
import inspect
import sys
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Iterator, List, Type

from .parsed_file import ParsedFile


class SupportedFileType(StrEnum):
    CSV = "csv"
    JSON = "json"

    @classmethod
    def list_values(cls) -> str:
        """Returns a comma-separated string of enum values with quotes."""
        return ", ".join(f"'{item.value}'" for item in cls)

    @classmethod
    def __str__(cls) -> str:
        """String representation of the enum class."""
        return cls.list_values()

    def __repr__(self) -> str:
        """Representation of an enum instance."""
        return f"{self.__class__.__name__}.{self.name}"


# This allows list(SupportedFileType) to show pretty values
def __list_repr__(enum_class) -> List[str]:
    return [item.value for item in enum_class]


SupportedFileType.__list_repr__ = classmethod(__list_repr__)


class FileParser(ABC):
    @staticmethod
    def match_me(extension_str: SupportedFileType) -> bool:
        pass

    def __init__(self, file: str):
        self._file = file

    @abstractmethod
    def parse(self) -> ParsedFile:
        pass


class CSVParser(FileParser):
    @staticmethod
    def match_me(extension_str: str) -> bool:
        return extension_str == SupportedFileType.CSV

    def __init__(self, file: str):
        super().__init__(file=file)

    def parse(self) -> ParsedFile:
        print(f"CSV parse {self._file}")
        data: dict[str, list[str]] = {}
        with open(self._file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter=";")
            for row in csv_reader:
                for key, value in row.items():
                    if key not in data:
                        data[key] = []
                    data[key].append(value)

        return ParsedFile(data)


class JSONParser(FileParser):
    @staticmethod
    def match_me(extension_str: str) -> bool:
        return extension_str == SupportedFileType.JSON

    def __init__(self, file):
        super().__init__(file)

    def parse(self) -> ParsedFile:
        print(f"JSON parse {self._file}")


def supported_file_parsers() -> Iterator[Type[FileParser]]:
    # Get reference to current module
    current_module = sys.modules[__name__]

    for _, obj in inspect.getmembers(current_module):
        if (
            inspect.isclass(obj)
            and issubclass(obj, FileParser)
            and obj is not FileParser
        ):
            yield obj
