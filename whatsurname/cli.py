import fire
import json
import sys
from .analyzer import NameAnalyzer

class NameCLI:
    """
    Onomastic Intelligence Utility CLI
    """
    def analyze(self, name: str, json_output: bool = False):
        """
        Analyze a name.
        
        Args:
            name: The name to analyze.
            json_output: If True, output results as JSON.
        """
        analyzer = NameAnalyzer()
        try:
            result = analyzer(name=name)
            
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
                "reasoning": result.reasoning
            }
            
            if json_output:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                # Fallback to simple print if not json (though TUI is preferred for rich output)
                print(f"Analysis for {name}:")
                for k, v in data.items():
                    print(f"{k}: {v}")

        except Exception as e:
            err = {"error": f"Unexpected error: {str(e)}"}
            if json_output:
                print(json.dumps(err, indent=2))
            else:
                print(err)
            sys.exit(1)

def run():
    fire.Fire(NameCLI)
