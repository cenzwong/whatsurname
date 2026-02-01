import os
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
# from rich.layout import Layout # Unused
# from rich.live import Live # Unused

from analyzer import NameAnalyzer

# Initialize Rich Console
console = Console()

def display_header():
    console.print(Panel(
        Text("Onomastic Intelligence Utility", justify="center", style="bold magenta"),
        subtitle="Powered by DSPy & Ollama",
        border_style="cyan"
    ))

def display_results(name: str, result: Any):
    """Display analysis results in a structured table."""
    # Main Results Table
    table = Table(title=f"Analysis for [bold yellow]{name}[/bold yellow]", show_header=False, box=None)
    table.add_column("Field", style="cyan", justify="right")
    table.add_column("Value", style="white")

    table.add_row("First Name", result.first_name)
    if result.middle_name and result.middle_name.lower() not in ["none", ""]:
        table.add_row("Middle Name", result.middle_name)
    table.add_row("Last Name", result.last_name)
    table.add_section() # logical separator

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
    except (ValueError, TypeError):
        table.add_row("Confidence", str(result.confidence_score))

    console.print(Panel(table, border_style="blue", expand=False))
    
    # Reasoning Panel
    console.print(Panel(
        Text(result.reasoning, style="italic dim"),
        title="Reasoning Chain",
        border_style="green",
        expand=False
    ))

def main():
    try:
        # Initialize the analyzer (encapsulates DSPy/Ollama setup)
        analyzer = NameAnalyzer()
    except Exception as e:
        console.print(f"[bold red]Initialization Error[/bold red]: {e}")
        return

    display_header()
    console.print("[dim]Type 'quit' or 'exit' to stop[/dim]\n")

    while True:
        try:
            name = console.input("[bold green]Enter a name[/bold green]: ").strip()
            if name.lower() in ['quit', 'exit', '']:
                console.print("[yellow]Exiting...[/yellow]")
                break
            
            with console.status(f"[bold blue]Analyzing '{name}'...[/bold blue]", spinner="dots"):
                result = analyzer.analyze(name=name)
            
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
