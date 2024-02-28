from vantage import VantageClient
from printer import Printer, Printable, OutputType
from typing import Callable, Any
from vantage.exceptions import (
    VantageForbiddenError,
    VantageInvalidRequestError,
    VantageInvalidResponseError,
    VantageNotFoundError,
    VantageServiceError,
    VantageUnauthorizedError,
)

DEFAULT_API_HOST = "https://api.dev-a.dev.vantagediscovery.com"
DEFAULT_AUTH_HOST = "https://vantage-dev.us.auth0.com"

EXCEPTION_MESSAGES = {
    VantageInvalidRequestError: "Invalid request sent.",
    VantageForbiddenError: "Access denied. You are not authorized to perform this action.",
    VantageInvalidResponseError: "Service error, server returned erroneous response.",
    VantageNotFoundError: "Resource not found.",
    VantageUnauthorizedError: "Unauthorized. Check your credentials.",
    VantageServiceError: "Unknown error ocurred.",
}


def create_client(jwt_token: str, account_id: str):
    return VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        api_host=DEFAULT_API_HOST,
        account_id=account_id,
    )


def create_printer(output_type: str):
    return Printer(output_type=OutputType[output_type.upper()])


def get_generic_message_for_exception(exception: Exception) -> str:
    if type(exception) in EXCEPTION_MESSAGES:
        return EXCEPTION_MESSAGES[type(exception)]
    else:
        return exception.message
