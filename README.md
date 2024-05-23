<img src="assets/vantage_logo.png" title="Vantage Discovery Logo" width="300"/></br>

# vantage-cli

CLI application for accessing Vantage API. Application is implemented using Python, and [Vantage Python SDK](https://github.com/VantageDiscovery/vantage-sdk-python/).

## Features

CLI supports all of the Vantage API endpoints: account management, collections management, search, and API keys management.

## Installation

### Binary

Grab latest binary from our [releases](https://github.com/VantageDiscovery/vantage-cli/releases) page, and extract it into your PATH.

### Building your own binary using Pyinstaller

1. Clone this repository using git, or download and unpack [ZIP file](https://github.com/VantageDiscovery/vantage-cli/archive/refs/heads/develop.zip).
2. Create virtual environment to build the binary *[Optional]*
3. Run `poetry install --all-extras` in the root of the directory
4. Deactivate and activate your virtual environment *[Optional]*
5. Run `pyinstaller -F vantage_cli/vantage.py`

Binary named `vantage` will be built in the `dist` directory. Copy it into your PATH.

### Source

It is recommended to use a binary, but if for whatever reason you need to use this software from source, you can do it in following way.

1. Clone this repository using git, or download and unpack [ZIP file](https://github.com/VantageDiscovery/vantage-cli/archive/refs/heads/develop.zip).
2. Ensure that you have `Python 3.10`, and `poetry` tool installed, either locally, or use virtual environment.
3. Run `poetry install` in the root of the cli directory.
4. Run `python vantage_sdk/vantage.py` from the root directory.

## Usage

If running for the first time, CLI will ask you a few questions to create initial configuration file, and then show help.

Generally, CLI usage is like following:

```bash
vantage [GENRAL_OPTIONS] command [COMMAND_OPTIONS] [COMMAND_ARGUMENTS]
```

For example:

```bash
vantage -o csv -a example-account create-collection --collection-id example --collection-name "My example collection" --embeddings-dimension 1536 --use-provided-embeddings true
```

### Getting help

Run `vantage --help` to show available options and commands.

Each command has specific help available, run `vantage command --help` to get help for each one of them

For example, running:

```bash
vantage create-collection-openai --help
```

Will output following help text:

```text
Usage: vantage create-collection-openai [OPTIONS]

  Creates a new OpenAI collection.

Options:
  --collection-id TEXT            ID for the new collection.  [required]
  --collection-name TEXT          Name for the new collection.  [required]
  --llm-secret TEXT               OpenAI account secret key.
  --llm-model-name TEXT           OpenAI LLM model name.
  --external-account-id TEXT      OpenAI account key ID from Vantage Console.
  --secondary-external-account-id TEXT
                                  Secondary external LLM account key ID.
  --collection-preview-url-pattern TEXT
                                  URL pattern for previewing items in the
                                  collection.
  --embeddings-dimension INTEGER  Dimension of the embeddings stored in the
                                  collection.
  --help                          Show this message and exit.
```

### Debug messages

When running Vantage CLI with `-d` switch, it will print out debug messages to STDERR, which can be useful when troubleshooting issues.

For example, `vantage -d list-collections` will output something like this:

```text
[2024-05-23 15:49:02] DEBUG [vantage.vantage.cli:228] Invoked command list-collections
[2024-05-23 15:49:02] DEBUG [vantage.vantage.cli:229] Using API host: https://api.vanta.ge
[2024-05-23 15:49:02] DEBUG [vantage.vantage.cli:230] Using account ID: test
[2024-05-23 15:49:02] DEBUG [vantage.vantage.cli:235] Creating client using API key: $2a$********************************************************
[2024-05-23 15:49:02] DEBUG [vantage.collections.list_collections:34] Listing collections...
[
  {
    "collection_id": "test-collection",
    "embeddings_dimension": 1536,
    "user_provided_embeddings": false,
    "collection_name": "test-collection",
    "collection_state": "Active",
    "collection_status": "Online",
    "collection_created_time": "2024-03-06T10:53:07",
    "collection_preview_url_pattern": "test/test-collection"
  }
]
```

In case that something goes wrong when running a command, using debug switch will print more details about error that occurred, including stacktrace.

## Configuration

### Location

Configuration file location depends on OS you are using. Most commonly locations are:

**Windows**: `C:\Users\user\AppData\Local\vantage-cli\config.ini`

**Mac OS**: `/Users/user/Library/Application Support/vantage-cli/config.ini`

**Linux/BSD/Other Unix**: `/home/user/.config/vantage-cli/config.ini`

### Format

Configuration is stored as `.ini` file:

```ini
[general]
client_id = <client id>
client_secret = <client secret>

[general.search]
vantage_api_key = <API key>

```

If no configuration file is present, CLI will ask you for M2M credentials, and API key, as a minimum. All of these parameters can be overridden using CLI options at runtime.

Options in the configuration file have the same name as runtime options, except that dash is replaced by underscore:

```bash
vantage --account-id example
```

Will translate to configuration like this:

```ini
[general]
account_id = example
```

#### Section `general`
**general** section contains options passed to the CLI at runtime. You can see the available options by running `./vantage.py --help`.


#### Section `general.search`

**general.search** section contains options common to all of the search commands.

For example, setting `accuracy` parameter in this section, will set it as common for all of the search commands:

```ini
[general.search]
accuracy = 0.4
```

When running any of the search commands, for example:

```bash
vantage semantic-search --collection-id example-collection lamp
```

It will be the same as you've ran:

```bash
vantage semantic-search --collection-id example-collection --accuracy 0.4 lamp
```

> Note that you can override options from `general.search` section by adding new section for a specific search command, with the overriden option:

```ini
[general.search]
accuracy = 0.4

[more-like-this-search]
accuracy = 0.3 # This will override the value above
```

#### Commands section

It is possible to set default values in configuration file for all of the other commands.

For example, setting default `--items-per-page` for `semantic-search` command would look like this:

```ini
[semantic-search]
items_per_page = 20
```

Note that when specifying command section, dash in the command name will not get converted to underscore, as when specifying options.