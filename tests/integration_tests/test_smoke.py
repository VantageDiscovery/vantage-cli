from vantage_cli.cli import cli
from click.testing import CliRunner


class TestAccount:
    def test_get_account(self, config_path) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["-c", config_path, "get-account"])
        assert result.exit_code == 0


class TestCollection:
    def test_create_collection(self, config_path) -> None:
        pass
