from abc import ABC, abstractmethod

import jsonpickle
from vantage import Vantage


class Printable(ABC):
    def print(self) -> None: ...


class Command(ABC):
    def __init__(self, client: Vantage, **kwargs):
        self.client = client
        self.kwargs = kwargs

    @abstractmethod
    def _execute(self) -> object: ...

    def _parse(self, output: object) -> str:
        return jsonpickle.dumps(output, unpicklable=False)

    def execute(self) -> str:
        return self._parse(self._execute())


class GetAccount(Command):
    def __init__(self, client: Vantage, **kwargs):
        Command.__init__(self, client=client, kwargs=kwargs)

    def _execute(self) -> str:
        return self.client.get_account().__dict__


class CommandParser:
    commands = {"get-account": GetAccount}

    def __init__(self, client: Vantage):
        self.client = client

    def parse(self, command: str, **kwargs) -> Command:
        klass = self.commands.get(command)

        if not issubclass(klass, Command):
            # Should never happen.
            raise ValueError("Invalid type class.")

        if not klass:
            # Should never happen, it means that command is not implemented.
            raise ValueError("Invalid command.")

        instance = klass.__new__(klass)
        instance.__init__(client=self.client, kwargs=kwargs)  # type: ignore
        return instance
