from typing import Callable, Optional, Type
from printer import Printable, ContentType, Printer
import traceback
from vantage.exceptions import (
    VantageForbiddenError,
    VantageInvalidRequestError,
    VantageInvalidResponseError,
    VantageNotFoundError,
    VantageServiceError,
    VantageUnauthorizedError,
)
from vantage.model.search import MoreLikeTheseItem
import jsonpickle


class CommandExecutor:
    EXCEPTION_MESSAGES = {
        VantageInvalidRequestError: "Invalid request sent.",
        VantageForbiddenError: "Access denied. You are not authorized to perform this action.",
        VantageInvalidResponseError: "Service error, server returned erroneous response.",
        VantageNotFoundError: "Resource not found.",
        VantageUnauthorizedError: "Unauthorized. Check your credentials.",
        VantageServiceError: "Unknown error ocurred.",
    }

    def __init__(self, debug_exceptions: bool = False):
        self.debug_exceptions = debug_exceptions

    def get_generic_message_for_exception(self, exception: Exception) -> str:
        if type(exception) in self.EXCEPTION_MESSAGES:
            return self.EXCEPTION_MESSAGES[type(exception)]
        else:
            return exception

    def execute_and_print_output(
        self,
        command: Callable,
        output_type: ContentType,
        printer: Printer,
        exception_handler: Optional[Callable] = None,
    ) -> None:
        printable = None

        try:
            printable = Printable(
                content=command(),
                content_type=output_type,
            )
        except Exception as exception:
            if self.debug_exceptions:
                print(traceback.format_exc())
                return

            if exception_handler:
                printable = exception_handler(exception)
            if not printable:
                printable = Printable(
                    content=self.get_generic_message_for_exception(exception),
                    content_type=ContentType.PLAINTEXT,
                )
        printer.print(printable)


def specific_exception_handler(
    exception: Exception, class_type: Type, message: str
) -> Printable:
    if isinstance(exception, class_type):
        return Printable(
            content="Collection not found.",
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
