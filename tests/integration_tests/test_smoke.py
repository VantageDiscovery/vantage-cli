from vantage_cli.vantage import cli
import time
import jsonpickle


class TestAccount:
    def test_get_account(self, config_path, runner) -> None:
        # When
        result = runner.invoke(cli, ["-c", config_path, "get-account"])

        # Then
        assert result.exit_code == 0


class TestCollections:

    def test_create_collection(
        self, config_path, random_string_generator, runner
    ) -> None:
        # Given
        collection_id = random_string_generator(10)
        collection_name = random_string_generator(10)

        # When
        result = runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "create-collection",
                "--collection-id",
                collection_id,
                "--collection-name",
                collection_name,
                "--embeddings-dimension",
                1536,
                "--use-provided-embeddings",
                "true",
            ],
        )

        # Then
        assert result.exit_code == 0

        # After
        time.sleep(1)
        result = runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "delete-collection",
                collection_id,
            ],
        )

    def test_delete_collection(
        self, config_path, random_string_generator, runner
    ) -> None:
        # Given
        collection_id = random_string_generator(10)
        collection_name = random_string_generator(10)
        runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "create-collection",
                "--collection-id",
                collection_id,
                "--collection-name",
                collection_name,
                "--embeddings-dimension",
                1536,
                "--use-provided-embeddings",
                "true",
            ],
        )
        time.sleep(1)

        # When
        result = runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "delete-collection",
                collection_id,
            ],
        )

        # Then
        assert result.exit_code == 0

    def test_list_collections(
        self, config_path, random_string_generator, runner
    ) -> None:
        # Given
        runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "list-collections",
            ],
        )

        # When
        result = runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "list-collections",
            ],
        )

        # Then
        assert result.exit_code == 0
        collections = jsonpickle.loads(result.stdout)
        assert len(collections) > 0


class TestKeys:
    def test_get_vantage_api_keys(self, config_path, runner) -> None:
        # When
        result = runner.invoke(
            cli, ["-c", config_path, "get-vantage-api-keys"]
        )

        # Then
        assert result.exit_code == 0

    def test_get_external_api_keys(self, config_path, runner) -> None:
        # When
        result = runner.invoke(
            cli, ["-c", config_path, "get-external-api-keys"]
        )

        # Then
        assert result.exit_code == 0


class TestSearch:
    def test_embedding_search(
        self, config_path, search_test_collection, runner
    ) -> None:
        # When
        result = runner.invoke(
            cli,
            [
                "-c",
                config_path,
                "embedding-search",
                "--collection-id",
                search_test_collection,
                str([0.1 for col in range(1536)]),
            ],
        )

        # Then
        assert result.exit_code == 0
