# Onomastic Intelligence Utility

A utility for analyzing names with DSPy and an OpenAI-compatible language model endpoint. It reports name breakdown, meaning, original script, ethnicity, geography, gender, confidence, and reasoning.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended)
- A running OpenAI-compatible API endpoint

## Install

```bash
pipx install git+https://github.com/cenzwong/whatsurname.git
```

For a source checkout:

```bash
git clone https://github.com/cenzwong/whatsurname.git
cd whatsurname
uv sync
```

## Default: Apple Foundation Models

Install and launch Apple's Foundation Models server with `fm serve`. The default endpoint is `http://127.0.0.1:1976/v1`, using model ID `system` and API key `not-needed`.

```bash
fm serve
whatsurname models
whatsurname analyze "Tsz Ho Wong" --json_output
whatsurname
```

The `models` command lists model IDs served by the configured endpoint and marks the selected model.

## Configure another provider

Set the OpenAI-compatible API's base URL, model ID, and API key in your environment or a project `.env` file:

```bash
export WHATSURNAME_BASE_URL=https://api.example.com/v1
export WHATSURNAME_MODEL=your-model-id
export WHATSURNAME_API_KEY=your-api-key
```

The base URL is normalized by removing trailing slashes. Existing shell environment values take precedence over values in `.env`. The API key is sent as bearer authentication for model discovery and used for analysis.

You can also put these values in `.env`:

```env
WHATSURNAME_BASE_URL=https://api.example.com/v1
WHATSURNAME_MODEL=your-model-id
WHATSURNAME_API_KEY=your-api-key
```

## Use the CLI and TUI

Analyze a name and preserve the JSON fields used for pipeline integration:

```bash
whatsurname analyze "Tsz Ho Wong" --json_output
```

Start the interactive terminal UI:

```bash
whatsurname
```

The TUI subtitle shows the active model. Type a name and press Enter to analyze it; type `quit` or `exit` to close.

## Library usage

```python
from whatsurname import NameAnalyzer

analyzer = NameAnalyzer()
result = analyzer("Svetlana Kuznetsova")
print(result.first_name, result.likely_gender, result.geographic_origin)
```

Constructor overrides are available for applications that need per-instance configuration:

```python
analyzer = NameAnalyzer(
    model="your-model-id",
    base_url="https://api.example.com/v1",
    api_key="your-api-key",
)
```
