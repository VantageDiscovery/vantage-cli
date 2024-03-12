import os
from typing import Optional, Callable
import pytest
import string
import random
from click.testing import CliRunner

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ABS_PATH, os.pardir, os.pardir))


def _random_string(length: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="module")
def random_string_generator() -> Callable:
    return _random_string


@pytest.fixture(scope="module")
def config_path() -> Optional[str]:
    config_path = os.path.join(
        PROJECT_DIR, "tests", "integration_tests", ".test_data", "config.ini"
    )
    if not os.path.exists(config_path):
        pytest.skip(f"No test config file available in {str(config_path)}.")

    return str(config_path)
