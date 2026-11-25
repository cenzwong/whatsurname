import dspy
from typing import Literal

from .config import get_model_config


class OnomasticAnalyzerSignature(dspy.Signature):
    """Analyze a name to determine its likely origin, ethnicity, gender, and meaning."""

    name = dspy.InputField(desc="The full name string (e.g., 'Mikhail')")

    first_name: str = dspy.OutputField(desc="Given name")
    middle_name: str = dspy.OutputField(desc="Middle name(s) if present, else empty string")
    last_name: str = dspy.OutputField(desc="Family name / Surname")

    literal_meaning: str = dspy.OutputField(desc="Semantic definition of the name")
    original_script: str = dspy.OutputField(desc="The name in its native script")
    ethnic_background: str = dspy.OutputField(desc="The specific ethno-cultural group")
    geographic_origin: str = dspy.OutputField(desc="Region or country where the name is most rooted")
    likely_gender: Literal["Masculine", "Feminine", "Unisex", "Undetermined"] = dspy.OutputField(
        desc="Masculine, Feminine, Unisex, or Undetermined"
    )
    confidence_score: float = dspy.OutputField(desc="Float from 0.0 to 1.0 indicating confidence")
    reasoning: str = dspy.OutputField(desc="Reasoning justifying the results")


class NameAnalyzer(dspy.Module):
    """DSPy module that analyzes the meaning, origin, ethnicity, and gender of names."""

    def __init__(
        self,
        model=None,
        base_url=None,
        api_key=None,
        *,
        model_name=None,
        api_base=None,
    ):
        """Create an analyzer; explicit settings override environment configuration.

        model_name and api_base are accepted as aliases for older callers.
        """
        super().__init__()
        settings = get_model_config(
            model=model if model is not None else model_name,
            base_url=base_url if base_url is not None else api_base,
            api_key=api_key,
        )
        self.model = settings["model"]
        self.base_url = settings["base_url"]
        self.api_key = settings["api_key"]

        # The current model setting is an OpenAI-compatible model ID, while
        # older callers may pass a DSPy provider-qualified value to model_name.
        legacy_provider_model = model is None and model_name and "/" in model_name
        lm_model = self.model if legacy_provider_model else f"openai/{self.model}"
        self.lm = dspy.LM(
            lm_model,
            api_base=self.base_url,
            api_key=self.api_key,
        )
        self.predictor = dspy.ChainOfThought(OnomasticAnalyzerSignature)

    def __call__(self, name: str):
        # DSPy's context is scoped to this invocation, so independent analyzer
        # instances do not replace each other's configured language model.
        with dspy.context(lm=self.lm):
            return self.predictor(name=name)
