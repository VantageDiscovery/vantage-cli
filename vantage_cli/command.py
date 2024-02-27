from abc import ABC, abstractmethod
from printer import Printable, ContentType
from vantage import VantageClient


class CommandArgument:
    def __init__(self, name: str, description: str, is_mandatory: bool = True):
        self.name = name
        self.description = description
        self.is_mandatory = is_mandatory


class Command(ABC):
    def __init__(self, client: VantageClient, args: dict):
        self.client = client
        self.args = args
        self._validate()

    @abstractmethod
    def _required_arguments(self) -> list[CommandArgument]: ...

    def _validate(self):
        for arg in self._required_arguments():
            if arg.is_mandatory and arg.name not in self.args.keys():
                raise ValueError(f"Missing required argument \"{arg.name}\".")

    @abstractmethod
    def execute(self) -> Printable: ...


class GetAccount(Command):

    def __init__(self, client: VantageClient, **args):
        Command.__init__(self, client=client, args=args)

    def _required_arguments(self) -> list[CommandArgument]:
        return []

    def execute(self) -> Printable:
        return Printable(
            content=self.client.get_account().__dict__,
            content_type=ContentType.OBJECT,
        )


class UpdateAccount(Command):

    def __init__(self, client: VantageClient, **args):
        Command.__init__(self, client=client, args=args)

    def _required_arguments(self) -> list[CommandArgument]:
        return [CommandArgument(name="name", description="Account name.")]

    def execute(self) -> Printable:
        arguments = self.args
        return Printable(
            self.client.update_account(
                account_name=arguments["name"]
            ).__dict__,
            content_type=ContentType.OBJECT,
        )


class GetVantageClientApiKeys(Command):

    def __init__(self, client: VantageClient, **args):
        Command.__init__(self, client=client, args=args)

    def _required_arguments(self) -> list[CommandArgument]:
        return []

    def execute(self) -> Printable:
        return Printable(
            content=[
                item.__dict__ for item in self.client.get_vantage_api_keys()
            ],
            content_type=ContentType.OBJECT,
        )


class GetVantageClientApiKey(Command):

    def __init__(self, client: VantageClient, **args):
        Command.__init__(self, client=client, args=args)

    def _required_arguments(self) -> list[CommandArgument]:
        return [CommandArgument(name="id", description="Vantage API key ID.")]

    def execute(self) -> Printable:
        key_id = self.args["id"]

        return Printable(
            content=self.client.get_vantage_api_key(
                vantage_api_key_id=key_id
            ).__dict__,
            content_type=ContentType.OBJECT,
        )


class CreateExternalApiKey(Command):

    def __init__(self, client: VantageClient, **args):
        Command.__init__(self, client=client, args=args)

    def _required_arguments(self) -> list[CommandArgument]:
        return [
            CommandArgument(
                name="llm_provider",
                description="LLM provider ID: [\"OpenAI\", \"HuggingFace\"]",
            ),
            CommandArgument(
                name="llm_secret", description="Secret key for LLM provider"
            ),
            # TODO: find out what is `url` parameter for.
            CommandArgument(
                name="url", description="LLM key URL", is_mandatory=False
            ),
        ]

    def execute(self) -> Printable:
        llm_provider = self.args["llm_provider"]
        llm_secret = self.args["llm_secret"]
        url = self.args["url"]

        return Printable(
            content=self.client.create_external_api_key(
                llm_provider=llm_provider,
                llm_secret=llm_secret,
                url=url,
            ).__dict__,
            content_type=ContentType.OBJECT,
        )


class CommandParser:
    commands = {
        "get-account": GetAccount,
        "update-account": UpdateAccount,
        "get-vantage-api-keys": GetVantageClientApiKeys,
        "get-vantage-api-key": GetVantageClientApiKey,
        "create-external-api-key": CreateExternalApiKey,
    }

    def __init__(self, client: VantageClient):
        self.client = client

    def _parse_arguments(self, **kwargs) -> list[dict[str, str]]:
        arguments_list = kwargs.get("command_arguments")
        arguments = {}
        for argument in arguments_list:
            key_value = argument.split("=")
            arguments[key_value[0]] = key_value[1]
        return arguments

    def parse(self, command: str, **kwargs) -> Command:
        klass = self.commands.get(command)

        if not issubclass(klass, Command):
            # Should never happen.
            raise ValueError("Invalid type class.")

        if not klass:
            # Should never happen, it means that command is not implemented.
            raise ValueError(f"Not implemented: {command}")

        command_arguments = self._parse_arguments(**kwargs)

        instance = klass.__new__(klass)
        instance.__init__(client=self.client, **command_arguments)  # type: ignore
        return instance
