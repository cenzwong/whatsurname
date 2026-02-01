import os
import dspy
from dotenv import load_dotenv

load_dotenv()

class OnomasticAnalyzerSignature(dspy.Signature):
    """Analyze a name to determine its likely origin, ethnicity, gender, and meaning."""
    
    name = dspy.InputField(desc="The full name string (e.g., 'Mikhail')")
    
    first_name = dspy.OutputField(desc="Given name")
    middle_name = dspy.OutputField(desc="Middle name(s) if present, else empty string")
    last_name = dspy.OutputField(desc="Family name / Surname")
    
    literal_meaning = dspy.OutputField(desc="Semantic definition of the name (e.g., 'Who is like God?')")
    original_script = dspy.OutputField(desc="The name in its native script (e.g., 'Михаил' or '三沢')")
    ethnic_background = dspy.OutputField(desc="The specific ethno-cultural group (e.g., Ashkenazi Jewish, Han Chinese)")
    geographic_origin = dspy.OutputField(desc="Region or country where the name is most rooted")
    likely_gender = dspy.OutputField(desc="Masculine, Feminine, Unisex, or Undetermined")
    confidence_score = dspy.OutputField(desc="Float from 0.0 to 1.0 indicating confidence in the analysis")
    reasoning = dspy.OutputField(desc="Step-by-step logic justifying the results")

class NameAnalyzer(dspy.Module):
    def __init__(self, model_name='ollama_chat/gpt-oss:120b-cloud', api_base='http://localhost:11434'):
        super().__init__()
        self.api_key = os.getenv("OLLAMA_API")
        self.lm = dspy.LM(model_name, api_base=api_base, api_key=self.api_key)
        dspy.configure(lm=self.lm)
        self.predictor = dspy.ChainOfThought(OnomasticAnalyzerSignature)

    def __call__(self, name: str):
        return self.predictor(name=name)
