import cli
import subprocess
from rich.console import Console

from cli.commands.stripe import stripe
from core.config import get_settings

console = Console()


DEFAULT_EVENTS = [
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
    "invoice.payment_succeeded",
    "invoice.payment_failed",
]


@stripe.command(name="listen")
@cli.option("--events", default=None, help="Events to listen for")
async def listen_webhooks(events: str | None) -> None:
    """Start listening to Stripe webhooks locally"""

    events_list = events.split(",") if events else DEFAULT_EVENTS

    settings = get_settings()
    forward_to = f"{settings.base_url}/webhooks/stripe"

    console.print(f"[yellow]🎧 Starting Stripe webhook listening to {forward_to}...[/yellow]")
    console.print("[cyan]The webhook secret will be displayed on startup[/cyan]")
    console.print("[red]Press Ctrl+C to stop[/red]\n")

    try:
        subprocess.run([
            "stripe",
            "listen",
            "--forward-to",
            forward_to,
            "--events",
            ",".join(events_list),
        ], check=True)

    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Listening stopped[/yellow]")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        console.print("[red]❌ Stripe CLI not installed or authentication error[/red]")
        console.print("Installation: [cyan]stripe login[/cyan]")
        console.print(e)
