import cli
import uvicorn

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.config import get_settings

console = Console()


@cli.command()
@cli.option('--host', default='0.0.0.0', help='Server host')
@cli.option('--port', default=8003, help='Server port')
@cli.option('--http-workers', default=None, help='Number of HTTP workers')
@cli.option('--reload/--no-reload', default=True, help='Enable/disable hot reload')
def serve(host: str, port: int, http_workers: int | None, reload: bool):
    """Starts the Server"""
    settings = get_settings()
    http_workers = settings.http_workers or http_workers
    http_workers = int(http_workers) if http_workers and not reload else None

    # Create a table for server information
    table = Table(title="Server Configuration")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Host", host)
    table.add_row("Port", str(port))
    table.add_row("Mode", "development" if reload else "production")
    table.add_row("HTTP Workers", str(http_workers or 'auto'))
    table.add_row("Log Level", settings.log_level.value)
    table.add_row("Log Output", settings.log_output.value)
    table.add_row("URL", f"http://{host}:{port}")

    # Display the table in a panel
    console.print(Panel(table, title=settings.title, border_style="blue"))

    # Start the server
    uvicorn.run(
        "main:app",
        factory=True,
        host=host,
        port=port,
        reload=reload,
        workers=http_workers,
        log_level=settings.log_level,
    )
