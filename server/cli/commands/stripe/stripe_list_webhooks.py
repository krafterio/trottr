import subprocess
import json
from rich.console import Console
from rich.table import Table

from cli.commands.stripe import stripe

console = Console()


@stripe.command(name="list-webhooks")
async def list_webhooks() -> None:
    """List all Stripe webhooks"""

    try:
        subprocess.run(["stripe", "--version"], check=True, capture_output=True)

        result = subprocess.run(
            ["stripe", "webhook_endpoints", "list"],
            check=True, capture_output=True, text=True
        )

        webhooks_data = json.loads(result.stdout)

        if not webhooks_data.get("data"):
            console.print("[yellow]No webhooks found[/yellow]")

            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=30)
        table.add_column("URL", style="green")

        for webhook in webhooks_data["data"]:
            webhook_id = webhook.get("id", "N/A")
            webhook_url = webhook.get("url", "N/A")
            table.add_row(webhook_id, webhook_url)

        console.print(f"[green]📋 Found {len(webhooks_data['data'])} Stripe Webhooks:[/green]")
        console.print(table)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        console.print("[red]❌ Stripe CLI not installed or authentication error[/red]")
        console.print("Use: [cyan]stripe login[/cyan]")
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ Error parsing JSON response: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
