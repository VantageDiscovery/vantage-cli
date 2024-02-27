from vantage import VantageClient
from printer import Printer, OutputType

DEFAULT_API_HOST = "https://api.dev-a.dev.vantagediscovery.com"
DEFAULT_AUTH_HOST = "https://vantage-dev.us.auth0.com"


def create_client(jwt_token: str, account_id: str):
    return VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        api_host=DEFAULT_API_HOST,
        account_id=account_id,
    )


def create_printer(output_type: str):
    return Printer(output_type=OutputType[output_type.upper()])
