import click
from configparser import ConfigParser
import platformdirs
import os
from typing import Optional
from pathlib import Path

CONFIG_FILE = "config.ini"
APP_NAME = "vantage-cli"
GENERAL_SECTION = "general"


def default_config_file() -> str:
    user_config_dir = platformdirs.user_config_dir(appname=APP_NAME)
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
        user_config_dir = platformdirs.user_config_dir(appname=APP_NAME)
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
    if config_loader.file_exists():
        config = config_loader.load()
        if GENERAL_SECTION in config.sections():
            ctx.default_map = dict(config[GENERAL_SECTION])
