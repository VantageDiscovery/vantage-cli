<img src="assets/vantage_logo.png" title="Vantage Discovery Logo" width="300"/></br>

# vantage-cli

CLI application for accessing Vantage API. Application is implemented using Python, and [Vantage Python SDK](https://github.com/VantageDiscovery/vantage-sdk-python/)

## Features

CLI supports all of the Vantage API endpoints: account management, collections management, search, and API keys management.

## Installation

1. Clone this repository using git, or download and unpack [ZIP file](https://github.com/VantageDiscovery/vantage-cli/archive/refs/heads/develop.zip).
2. Ensure that you have `Python 3.10`, and `poetry` tool installed, either locally, or use virtual environment.
3. Since we are currently fetching SDK from [test PyPi repository](https://test.pypi.org/project/vantage-sdk/), it is necessary to manually install it:
   1. Run `pip install pydantic==2.6.1 requests urllib3 python-dateutil` to install SDK requirements
   2. Run `pip install -i https://test.pypi.org/simple/ vantage-sdk==0.7.0` to install SDK.
4. Run `poetry install` in the root of the cli directory.

## Building binary using pyinstaller

1. Run `poetry install --all-extras` in the root of the directory
2. Run `pyinstaller vantage_cli/vantage.py`

Binary named `vantage` will be built in the `vantage_cli/dist/vantage` directory.

## Usage

If using source, enter the `vantage-cli/vantage_cli` directory, and run `./vantage.py --help`. CLI will ask you a few questions to create initial configuration file, and then show help.

If using binary, copy the binary from `vantage-cli/vantage_cli/dist/vantage` to your PATH, and use `vantage` binary instead of `vantage.py` script.

Generally, CLI usage is like following:

```bash
./vantage.py [GENRAL_OPTIONS] command [COMMAND_OPTIONS] [COMMAND_ARGUMENTS]
```

For example:

```bash
./vantage.py -o csv -a example-account create-collection --collection-id example --collection-name "My example collection" --embeddings-dimension 1536 --use-provided-embeddings true
```

### Getting help

Run `vantage.py --help` to show available options and commands.

Each command has specific help available, run `./vantage.py command --help` to get help for each one of them

For example, running:

```bash
./vantage.py create-collection --help
```

Will output following help text:

```bash
Usage: vantage.py create-collection [OPTIONS]

  Creates a new collection.

Options:
  --collection-id TEXT            ID for the new collection.  [required]
  --collection-name TEXT          Name for the new collection.  [required]
  --embeddings-dimension INTEGER  Collecion embedding dimension  [required]
  --llm-provider TEXT             LLM provider ID ("OpenAPI"|"Hugging")
  --external-key-id TEXT          Key for the external API
  --collection-preview-url-pattern TEXT
                                  URL pattern for previewing items in the
                                  collection
  --use-provided-embeddings BOOLEAN
                                  If the user will upload embeddings to
                                  collection afterwards.
  --help                          Show this message and exit.
```

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
./vantage.py --account-id example
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
./vantage.py semantic-search --collection-id example-collection lamp
```

It will be the same as you've ran:

```bash
./vantage.py semantic-search --collection-id example-collection --accuracy 0.4 lamp
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