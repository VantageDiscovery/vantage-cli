import click
from configparser import ConfigParser
import os
from typing import Optional
from pathlib import Path
from vantage_cli.commands.search import COMMAND_NAMES as search_commands


CONFIG_FILE = "config.ini"
APP_NAME = "vantage-cli"
GENERAL_SECTION = "general"
SEARCH_SECTION = "general.search"


def default_config_file() -> str:
    user_config_dir = click.get_app_dir(APP_NAME)
    return os.path.join(
        os.path.dirname(__file__), user_config_dir, CONFIG_FILE
    )


class ConfigLoader:
    def __init__(self, path: Optional[str] = None):
        if path is None:
            self.path = default_config_file()
        else:
            self.path = path

    def file_exists(self) -> bool:
        return Path(self.path).is_file()

    def load(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self.path)
        return config

    def initialize_file(self) -> None:
        user_config_dir = click.get_app_dir(APP_NAME)
        config_dir_path = Path(user_config_dir)
        if not config_dir_path.exists():
            os.mkdir(user_config_dir)
        else:
            if not config_dir_path.is_dir():
                raise ValueError(
                    f"{config_dir_path} exists and is not a directory!"
                )
        path = os.path.join(
            os.path.dirname(__file__), user_config_dir, CONFIG_FILE
        )
        with open(file=path, mode="w") as config_file:
            config_file.write("")
            config_file.close()

    @staticmethod
    def default() -> "ConfigLoader":
        return ConfigLoader()


class ConfigInitializer:

    def __init__(self, path: Optional[str] = None):
        if path is None:
            self.path = default_config_file()
        else:
            self.path = path

    def initialize_config(self):
        pass


def configuration_callback(ctx: click.core.Context, param, filename):
    config_loader = ConfigLoader(path=filename)

    if not config_loader.file_exists():
        click.echo("It seems that you have no config file. Running wizard...")
        initial_configuration_prompt(config_loader=config_loader)

    if config_loader.file_exists():
        config = config_loader.load()
        general_config = {}
        search_config = {}

        if GENERAL_SECTION in config.sections():
            general_config = dict(config[GENERAL_SECTION])

        if SEARCH_SECTION in config.sections():
            search_config = dict(config[SEARCH_SECTION])
            for command in search_commands:
                general_config[command] = search_config

        for section in config.sections():
            if section == GENERAL_SECTION or section == SEARCH_SECTION:
                continue
            if section in general_config:
                general_config[section] = general_config[section] | dict(
                    config[section]
                )
            else:
                general_config[section] = dict(config[section])

        ctx.default_map = general_config


def initial_configuration_prompt(config_loader: ConfigLoader) -> None:
    account_id = click.prompt(
        "Please enter Account ID (https://console.vanta.ge/account)", type=str
    )
    client_id = click.prompt(
        "Please enter Client ID (https://console.vanta.ge/account)", type=str
    )
    client_secret = click.prompt(
        "Please enter Client Secret (https://console.vanta.ge/account)",
        type=str,
    )
    api_key = click.prompt(
        "Please enter Vantage API key (https://console.vanta.ge/api)", type=str
    )

    config_loader.initialize_file()
    config = config_loader.load()
    config.add_section(GENERAL_SECTION)
    config.set(GENERAL_SECTION, "account_id", account_id)
    config.set(GENERAL_SECTION, "client_id", client_id)
    config.set(GENERAL_SECTION, "client_secret", client_secret)
    config.set(GENERAL_SECTION, "vantage_api_key", api_key)
    with open(config_loader.path, "w") as file:
        config.write(file, space_around_delimiters=True)
        file.close()
    click.echo(f"Created config file at {config_loader.path}")
