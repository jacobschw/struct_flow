"""
This module is to automize the
    1. extraction of values from structured file(s) (.csv, json)
    2. the creation of files storing the extracted data,
    3. merging a pair of files on key-relations
"""

from typing import List

import typer

from .file_parser import FileParser, SupportedFileType, supported_file_parsers
from .parsed_file import ParsedFile

app = typer.Typer()


class UnsupportedFileTypeError(ValueError):
    """Raised when trying to process a file with an unsupported extension."""

    pass


class FileProcessor:
    def __init__(self, file: str):
        self._extension = file.split(".")[-1]
        self._path = file

    def parse(self) -> ParsedFile:
        return self._parser().parse()

    def _parser(self) -> FileParser:
        for supported_parser in supported_file_parsers():
            if supported_parser.match_me(self._extension):
                return supported_parser(self._path)

        raise UnsupportedFileTypeError(
            f"Cannot process files with extension '{self._extension}'. Supported extensions: {list(SupportedFileType)}"
        )


@app.command()
def extract_from(
    file: str, fields: List[str] = typer.Argument(..., help="One or more field names")
):

    typer.echo(f"Processing file {file}")
    try:
        parsed_file = FileProcessor(file=file).parse()
        typer.echo(parsed_file)

        for field in fields:
            typer.echo(f"Processing field: {field}")

        typer.echo(f"Total fields processed: {len(fields)}")

    except UnsupportedFileTypeError as e:
        typer.echo(e)
        return 1
    except FileNotFoundError:
        typer.echo(f"Error: File {file} not found")
        return


if __name__ == "__main__":
    app()
