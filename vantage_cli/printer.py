from enum import Enum
from typing import Any
import jsonpickle
import csv
from io import StringIO
import click


class ContentType(Enum):
    OBJECT = "object"
    DICT = "dict"
    LIST = "list"
    PLAINTEXT = "plaintext"


class OutputType(Enum):
    JSON = "json"
    PLAINTEXT = "plaintext"
    CSV = "csv"


class Printable:

    def __init__(self, content: str | dict | list, content_type: ContentType):
        self.content = content
        self.content_type = content_type


class Printer:

    def __init__(self, output_type: OutputType):
        self.output_type = output_type

    def _to_json(self, content: dict[str, Any]) -> str:
        return jsonpickle.dumps(content, indent=2, unpicklable=False)

    def _to_csv(self, content: list[Any] | dict[str, Any]) -> str:
        data = StringIO()
        doc = csv.writer(data, lineterminator='\n')

        if isinstance(content, dict):
            doc.writerow(content.keys())
            doc.writerow(content.values())

        if isinstance(content, list):
            doc.writerow(content[0].keys())
            for item in content:
                doc.writerow(item.values())

        return data.getvalue()

    def parse(self, printable: Printable) -> str:
        if printable is None or printable.content is None:
            return ""
        if self.output_type == OutputType.JSON:
            return self._to_json(printable.content)
        elif self.output_type == OutputType.CSV:
            return self._to_csv(printable.content)
        elif self.output_type == OutputType.PLAINTEXT:
            return printable.content

    def print(self, content) -> None:
        click.echo(self.parse(content))
