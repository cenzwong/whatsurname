# Onomastic Intelligence Utility

A powerful, AI-driven utility for analyzing names to determine their origin, ethnicity, gender, meaning, and cultural background. Built with **DSPy** and **Ollama**.

## Features

-   **Deep Analysis**: Extracts literal meaning, original script, ethnic background, geography, and gender.
-   **Name Breakdown**: Automatically parses First, Middle, and Last names.
-   **Interactive TUI**: A beautiful terminal interface powered by `rich`.
-   **CLI Mode**: JSON output for pipeline integration.
-   **Library Support**: Use `NameAnalyzer` directly in your Python projects.

## Prerequisites

1.  **Python 3.13+**
2.  **uv** (recommended for dependency management)
3.  **Ollama** running locally with the `gpt-oss:120b-cloud` model (or configure your own in `analyzer.py`).

## Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/whatsurname.git
    cd whatsurname
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory with your Ollama API key (if required) or configuration:
    ```env
    OLLAMA_API=your_api_key_here
    ```

## Usage

### 1. Interactive TUI (Recommended)
Launch the interactive text user interface:

```bash
uv run whatsurname
```
*Or via python module:*
```bash
uv run python -m whatsurname.main
```

**Commands within TUI:**
-   Type a name and press Enter to analyze.
-   Type `quit` or `exit` to close.

### 2. CLI Mode (JSON Output)
For integration with other tools, use the CLI mode to get JSON output:

```bash
uv run whatsurname analyze "Tsz Ho Wong" --json_output
```

**Example Output:**
```json
{
  "name": "Tsz Ho Wong",
  "first_name": "Tsz Ho",
  "middle_name": "",
  "last_name": "Wong",
  "meaning": "Great aspiration (志浩)",
  "script": "黃志浩",
  "ethnicity": "Cantonese (Hong Kong)",
  "geography": "Hong Kong",
  "gender": "Masculine",
  "confidence": 0.85,
  "reasoning": "..."
}
```

### 3. Library Usage
You can use the `NameAnalyzer` class directly in your own Python scripts:

```python
from whatsurname import NameAnalyzer

# Initialize
analyzer = NameAnalyzer()

# Analyze a name
result = analyzer("Svetlana Kuznetsova")

# Access fields
print(f"First Name: {result.first_name}")
print(f"Gender: {result.likely_gender}")
print(f"Origin: {result.geographic_origin}")
```

## Project Structure

-   `whatsurname/`: Main package.
    -   `analyzer.py`: Core DSPy logic and `NameAnalyzer` class.
    -   `tui.py`: Interactive TUI logic (`rich`).
    -   `cli.py`: Command-line interface logic (`argparse`).
    -   `main.py`: Entry point dispatcher.
