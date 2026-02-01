import os
import dspy
from dotenv import load_dotenv

load_dotenv()

class OnomasticAnalyzerSignature(dspy.Signature):
    """
    Perform a deep cultural and linguistic analysis of a personal name.
    Identify literal meanings, original scripts, and demographic associations.
    """
    name = dspy.InputField(desc="The full name string (e.g., 'Mikhail')")
    
    first_name = dspy.OutputField(desc="Given name")
    middle_name = dspy.OutputField(desc="Middle name(s) if present, else empty string")
    last_name = dspy.OutputField(desc="Family name / Surname")
    
    literal_meaning = dspy.OutputField(desc="Semantic definition of the name (e.g., 'Who is like God?')")
    original_script = dspy.OutputField(desc="The name in its native script (e.g., 'Михаил' or '三沢')")
    ethnic_background = dspy.OutputField(desc="The specific ethno-cultural group (e.g., Ashkenazi Jewish, Han Chinese)")
    geographic_centroid = dspy.OutputField(desc="The primary country or region of historical origin")
    likely_gender = dspy.OutputField(desc="Masculine, Feminine, or Unisex (include probability if possible)")
    confidence_score = dspy.OutputField(desc="Float from 0.0 to 1.0 indicating confidence in the analysis")
    reasoning = dspy.OutputField(desc="Step-by-step logic justifying the results")

class NameAnalyzer:
    def __init__(self, model_name='ollama_chat/gpt-oss:120b-cloud', api_base='http://localhost:11434'):
        self.api_key = os.getenv("OLLAMA_API")
        self.lm = dspy.LM(model_name, api_base=api_base, api_key=self.api_key)
        dspy.configure(lm=self.lm)
        self.predictor = dspy.ChainOfThought(OnomasticAnalyzerSignature)

    def analyze(self, name: str):
        return self.predictor(name=name)
