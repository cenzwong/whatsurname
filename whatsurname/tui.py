from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Input, Static, Label
from textual.reactive import reactive
from rich.table import Table
from rich.panel import Panel
from .analyzer import NameAnalyzer

class NameAnalysisApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    
    Input {
        dock: top;
        margin: 1;
    }
    
    #results-container {
        padding: 1;
        height: 1fr;
    }
    
    .intro {
        text-align: center;
        color: $text-muted;
        margin: 2;
    }
    """
    
    TITLE = "Onomastic Intelligence"
    SUB_TITLE = "Powered by DSPy & Ollama"

    def __init__(self):
        super().__init__()
        self.analyzer = NameAnalyzer()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter a name to analyze (e.g. 'Mikhail')", id="name-input")
        with VerticalScroll(id="results-container"):
            yield Static("Welcome to Onomastic Intelligence. Enter a name above to begin.", id="output-area", classes="intro")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        name = event.value.strip()
        if not name:
            return
            
        output_widget = self.query_one("#output-area", Static)
        output_widget.update(Panel(f"Analyzing [bold]{name}[/bold]...", style="blue"))
        
        # In a real async app we'd run this in a worker, but for now we block simply
        # or use run_worker if we want to be fancy. Let's use run_worker to keep UI responsive.
        self.run_worker(self.perform_analysis(name), exclusive=True)

    async def perform_analysis(self, name: str):
        output_widget = self.query_one("#output-area", Static)
        try:
            # Run blocking analysis
            # Since analyzer is synchronous, we wrap it? 
            # Textual workers can run threaded.
            result = await self.run_in_thread(lambda: self.analyzer(name))
            
            # Build Rich Renderables
            table = Table(title=f"Analysis for [bold yellow]{name}[/bold yellow]", show_header=False, expand=True)
            table.add_column("Field", style="cyan", justify="right")
            table.add_column("Value", style="white")

            table.add_row("First Name", result.first_name)
            if result.middle_name and result.middle_name.lower() not in ["none", ""]:
                table.add_row("Middle Name", result.middle_name)
            table.add_row("Last Name", result.last_name)
            table.add_section() 

            table.add_row("Meaning", result.literal_meaning)
            table.add_row("Script", f"[bold]{result.original_script}[/bold]")
            table.add_row("Ethnicity", result.ethnic_background)
            table.add_row("Geography", result.geographic_origin)
            table.add_row("Gender", result.likely_gender)
            table.add_row("Confidence", str(result.confidence_score))
            
            # Combine table and reasoning
            content = render_group(
                Panel(table, border_style="green"),
                Panel(result.reasoning, title="Reasoning Chain", border_style="dim")
            )
            output_widget.update(content)
            
        except Exception as e:
            output_widget.update(Panel(f"[bold red]Error:[/bold red] {str(e)}", border_style="red"))

    async def run_in_thread(self, func):
        """Helper to run blocking sync code in a thread."""
        import asyncio
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func)

# Helper for grouping rich renderables since Console.group is not directly a renderable container 
# that behaves exactly like a single widget content sometimes, but rich.console.Group works.
from rich.console import Group as render_group

def run():
    app = NameAnalysisApp()
    app.run()
