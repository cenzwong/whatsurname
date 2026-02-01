import os
import dspy
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live

load_dotenv()

# Initialize Rich Console
console = Console()

class OnomasticAnalyzer(dspy.Signature):
    """
    Perform a deep cultural and linguistic analysis of a personal name.
    Identify literal meanings, original scripts, and demographic associations.
    """
    name = dspy.InputField(desc="The full name string (e.g., 'Mikhail')")
    
    literal_meaning = dspy.OutputField(desc="Semantic definition of the name (e.g., 'Who is like God?')")
    original_script = dspy.OutputField(desc="The name in its native script (e.g., 'Михаил' or '三沢')")
    ethnic_background = dspy.OutputField(desc="The specific ethno-cultural group (e.g., Ashkenazi Jewish, Han Chinese)")
    geographic_centroid = dspy.OutputField(desc="The primary country or region of historical origin")
    likely_gender = dspy.OutputField(desc="Masculine, Feminine, or Unisex (include probability if possible)")
    confidence_score = dspy.OutputField(desc="Float from 0.0 to 1.0 indicating confidence in the analysis")
    reasoning = dspy.OutputField(desc="Step-by-step logic justifying the results")

def display_header():
    console.print(Panel(
        Text("Onomastic Intelligence Utility", justify="center", style="bold magenta"),
        subtitle="Powered by DSPy & Ollama",
        border_style="cyan"
    ))

def display_results(name, result):
    # Main Results Table
    table = Table(title=f"Analysis for [bold yellow]{name}[/bold yellow]", show_header=False, box=None)
    table.add_column("Field", style="cyan", justify="right")
    table.add_column("Value", style="white")

    table.add_row("Meaning", result.literal_meaning)
    table.add_row("Script", f"[bold]{result.original_script}[/bold]")
    table.add_row("Ethnicity", result.ethnic_background)
    table.add_row("Geography", result.geographic_centroid)
    table.add_row("Gender", result.likely_gender)
    
    # Colorize confidence
    try:
        conf = float(result.confidence_score)
        conf_color = "green" if conf > 0.8 else "yellow" if conf > 0.5 else "red"
        table.add_row("Confidence", f"[{conf_color}]{conf:.2f}[/{conf_color}]")
    except:
        table.add_row("Confidence", str(result.confidence_score))

    console.print(Panel(table, border_style="blue", expand=False))
    
    # Reasoning Panel (Collapsible concept, but just printed nicely here)
    console.print(Panel(
        Text(result.reasoning, style="italic dim"),
        title="Reasoning Chain",
        border_style="green",
        expand=False
    ))

def main():
    api_key = os.getenv("OLLAMA_API")
    # Configure DSPy with Ollama
    lm = dspy.LM('ollama_chat/gpt-oss:120b-cloud', api_base='http://localhost:11434', api_key=api_key)
    dspy.configure(lm=lm)
    
    name_analyzer = dspy.ChainOfThought(OnomasticAnalyzer)

    display_header()
    console.print("[dim]Type 'quit' or 'exit' to stop[/dim]\n")

    while True:
        try:
            name = console.input("[bold green]Enter a name[/bold green]: ").strip()
            if name.lower() in ['quit', 'exit', '']:
                console.print("[yellow]Exiting...[/yellow]")
                break
            
            with console.status(f"[bold blue]Analyzing '{name}'...[/bold blue]", spinner="dots"):
                result = name_analyzer(name=name)
            
            console.print() # Spacer
            display_results(name, result)
            console.print() # Spacer
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Error[/bold red]: {e}")

if __name__ == "__main__":
    main()
