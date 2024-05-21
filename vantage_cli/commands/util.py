from logging import Logger
from typing import Callable, Optional, Type
from vantage_cli.printer import Printable, ContentType, Printer
import traceback
from vantage_sdk.model.search import MoreLikeTheseItem
import jsonpickle


def mask_sensitive_string(value: str) -> str:
    if value is None:
        return value

    if len(value) < 8:
        return "*" * len(value)

    header = value[0:4]
    mask = "*" * (len(value) - 4)

    return header + mask


def get_generic_message_for_exception(exception: Exception) -> str:
    if hasattr(exception, "body") and exception.body is not None:
        return jsonpickle.loads(exception.body)
    if hasattr(exception, "reason") and exception.reason is not None:
        return f"Error: {exception.reason}"
    elif hasattr(exception, "args") and len(exception.args) > 0:
        text = "\n".join(exception.args)
        return f"Error: {text}"
    else:
        return "Error: Unknown error."


class CommandExecutor:
    def __init__(self, logger: Logger, debug: bool = False):
        self.debug = debug
        self.logger = logger

    def execute_and_print_output(
        self,
        command: Callable,
        output_type: ContentType,
        printer: Printer,
        exception_handler: Optional[Callable] = None,
    ) -> None:
        printable = None

        try:
            printable = Printable.stdout(
                content=command(),
                content_type=output_type,
            )
        except Exception as exception:
            self.logger.debug(traceback.format_exc())

            if exception_handler:
                printable = exception_handler(exception)
            if not printable:
                printable = Printable.stderr(
                    content=get_generic_message_for_exception(exception),
                    content_type=ContentType.PLAINTEXT,
                )
        printer.print(printable)

    def execute_and_print_printable(
        self,
        command: Callable,
        output_type: ContentType,
        printer: Printer,
        exception_handler: Optional[Callable] = None,
    ) -> None:
        printable = None

        try:
            printable = command()
        except Exception as exception:
            self.logger.debug(traceback.format_exc())

            if exception_handler:
                printable = exception_handler(exception)
            if not printable:
                printable = Printable.stderr(
                    content=get_generic_message_for_exception(exception),
                    content_type=ContentType.PLAINTEXT,
                )
        printer.print(printable)


def specific_exception_handler(
    exception: Exception, class_type: Type, message: str
) -> Printable:
    if isinstance(exception, class_type):
        return Printable.stderr(
            content=message,
            content_type=ContentType.PLAINTEXT,
        )
    else:
        return None


def parse_more_like_these(json_string: str) -> list[MoreLikeTheseItem]:
    data = jsonpickle.loads(json_string)

    return [
        MoreLikeTheseItem(weight=item["weight"], query_text=item["text"])
        for item in data
    ]
