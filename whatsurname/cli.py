import fire
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .analyzer import NameAnalyzer
from .config import get_model_config


class NameCLI:
    """Onomastic Intelligence Utility CLI."""

    def analyze(self, name: str, json_output: bool = False):
        """Analyze a name; optionally print the existing JSON output shape."""
        try:
            result = NameAnalyzer()(name=name)
            data = {
                "name": name,
                "first_name": result.first_name,
                "middle_name": result.middle_name,
                "last_name": result.last_name,
                "meaning": result.literal_meaning,
                "script": result.original_script,
                "ethnicity": result.ethnic_background,
                "geography": result.geographic_origin,
                "gender": result.likely_gender,
                "confidence": result.confidence_score,
                "reasoning": result.reasoning,
            }
            if json_output:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(f"Analysis for {name}:")
                for key, value in data.items():
                    print(f"{key}: {value}")
        except Exception as exc:
            if json_output:
                print(json.dumps({"error": f"Unexpected error: {exc}"}, indent=2))
            else:
                print(f"Unexpected error: {exc}", file=sys.stderr)
            sys.exit(1)

    def models(self):
        """List model IDs exposed by the configured OpenAI-compatible endpoint."""
        settings = get_model_config()
        url = f"{settings['base_url']}/models"
        request = Request(
            url,
            headers={"Authorization": f"Bearer {settings['api_key']}", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            message = f"Model discovery failed: HTTP {exc.code} {exc.reason}"
            if detail:
                message += f" — {detail}"
            print(message, file=sys.stderr)
            sys.exit(1)
        except URLError as exc:
            print(f"Could not connect to model endpoint {url}: {exc.reason}", file=sys.stderr)
            sys.exit(1)
        except (TimeoutError, OSError) as exc:
            print(f"Could not connect to model endpoint {url}: {exc}", file=sys.stderr)
            sys.exit(1)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(f"Invalid JSON response from model endpoint {url}: {exc}", file=sys.stderr)
            sys.exit(1)

        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            print("Invalid model-list response: expected an object with a 'data' array.", file=sys.stderr)
            sys.exit(1)

        models = []
        for item in payload["data"]:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
                print("Invalid model-list response: every data entry must have a non-empty string 'id'.", file=sys.stderr)
                sys.exit(1)
            models.append(item["id"])

        if not models:
            print("No models returned by the configured endpoint.")
            return
        for model_id in models:
            marker = " (selected)" if model_id == settings["model"] else ""
            print(f"{model_id}{marker}")


def run():
    fire.Fire(NameCLI)
