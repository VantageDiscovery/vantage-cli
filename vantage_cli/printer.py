from enum import Enum
from typing import Any
import jsonpickle
import csv
from io import StringIO
import sys
from dataclasses import dataclass


class ContentType(Enum):
    OBJECT = "object"
    DICT = "dict"
    LIST = "list"
    PLAINTEXT = "plaintext"


class OutputFormat(Enum):
    JSON = "json"
    PLAINTEXT = "plaintext"
    CSV = "csv"


class PrinterOutput(Enum):
    STDOUT = "stdout"
    STDERR = "stderr"


@dataclass(frozen=True)
class Printable:
    content: str | dict | list
    content_type: ContentType
    printer_output: PrinterOutput

    @staticmethod
    def stdout(
        content: str | dict | list,
        content_type: ContentType,
    ):
        return Printable(
            content=content,
            content_type=content_type,
            printer_output=PrinterOutput.STDOUT,
        )

    @staticmethod
    def stderr(
        content: str | dict | list,
        content_type: ContentType,
    ):
        return Printable(
            content=content,
            content_type=content_type,
            printer_output=PrinterOutput.STDERR,
        )


class Printer:

    def __init__(self, output_type: OutputFormat):
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
        if self.output_type == OutputFormat.JSON:
            return self._to_json(printable.content)
        elif self.output_type == OutputFormat.CSV:
            return self._to_csv(printable.content)
        elif self.output_type == OutputFormat.PLAINTEXT:
            return printable.content

    def print(self, content: Printable) -> None:
        if PrinterOutput.STDOUT.name == content.printer_output.name:
            self.stdout(self.parse(content))
        elif PrinterOutput.STDERR.name == content.printer_output.name:
            self.stderr(self.parse(content))
        else:
            self.stderr(
                f"warning: unknown output type: {content.printer_output}"
            )
            self.stdout(self.parse(content))

    def stdout(self, text: str) -> None:
        print(text, file=sys.stdout)

    def stderr(self, text: str) -> None:
        print(text, file=sys.stderr)

    def print_text(self, text) -> None:
        self.print(
            Printable(
                content=text,
                content_type=ContentType.PLAINTEXT,
                printer_output=PrinterOutput.STDOUT,
            )
        )


def create_printer(output_type: str):
    return Printer(output_type=OutputFormat[output_type.upper()])
