import cli
import subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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

@stripe.command(name="webhook-token")
@cli.option("--create", is_flag=True, help="Create a new webhook endpoint with Stripe CLI")
@cli.option("--events", default=None, help="Events to listen for")
async def webhook_token(create: bool, events: str | None) -> None:
    """Display the Stripe webhook token to configure in .env"""

    events_list = events.split(",") if events else DEFAULT_EVENTS

    settings = get_settings()
    webhook_url = f"{settings.base_url}/webhooks/stripe"

    if settings.stripe_webhook_secret:
        console.print(Panel.fit(
            f"[green]Current webhook token:[/green]\n[yellow]{settings.stripe_webhook_secret}[/yellow]",
            title="🔐 Stripe Webhook Token",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[red]No webhook token configured in STRIPE_WEBHOOK_SECRET[/red]",
            title="❌ Missing Token",
            border_style="red"
        ))

    console.print(f"\n[bold cyan]📡 Webhook URL:[/bold cyan] {webhook_url}")
    console.print("\n[bold blue]📋 Configuration Instructions:[/bold blue]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Method", style="cyan")
    table.add_column("Environment", style="yellow")
    table.add_column("Action", style="green")

    table.add_row(
        "Stripe CLI",
        "All environments",
        f"./kt stripe webhook-token --create"
    )

    table.add_row(
        "Stripe Dashboard",
        "Manual alternative",
        f"1. Go to Developers > Webhooks\n2. Create an endpoint\n3. Use URL: {webhook_url}\n4. Copy the signing secret"
    )

    console.print(table)

    console.print("\n[bold yellow]💡 Recommendation:[/bold yellow]")
    console.print("• [green]Use Stripe CLI[/green] for both development and production")
    console.print("• [yellow]Use Dashboard[/yellow] only if you prefer manual setup")
    console.print("• Make sure to use the correct Stripe account (test vs live)")

    if create:
        await create_webhook_endpoint(webhook_url, events_list)


async def create_webhook_endpoint(url: str, events_list: list[str]) -> None:
    """Create a webhook endpoint with Stripe CLI"""

    console.print(f"\n[yellow]🔄 Creating webhook endpoint for {url}...[/yellow]")

    try:
        subprocess.run(["stripe", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("[red]❌ Stripe CLI not installed![/red]")
        console.print("\n[bold]Installation required:[/bold]")
        console.print("• macOS: [cyan]brew install stripe/stripe-cli/stripe[/cyan]")
        console.print("• Linux: [cyan]curl -s https://packages.stripe.com/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg[/cyan]")
        console.print("• Windows: [cyan]scoop install stripe[/cyan]")
        console.print("\nThen: [cyan]stripe login[/cyan]")

        return

    try:
        cmd = [
            "stripe",
            "webhook_endpoints",
            "create",
            "--url",
            url,
            "--description",
            "Webhook for Smashr",
        ]

        all_events = []

        for event in events_list:
            all_events.extend([e.strip() for e in event.split(",")])

        cmd.extend(["--enabled-events", ",".join(all_events)])

        console.print(f"[dim]Executing: {' '.join(cmd)}[/dim]")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        console.print("[green]✅ Webhook created successfully![/green]")
        console.print(f"[dim]Response: {result.stdout}[/dim]")

        output_lines = result.stdout.strip().split('\n')
        webhook_id = None

        for line in output_lines:
            if line.startswith('we_'):
                webhook_id = line.strip()
                break

        if webhook_id:
            console.print(f"[cyan]Webhook ID: {webhook_id}[/cyan]")

            await get_webhook_secret(webhook_id)
        else:
            console.print("[yellow]⚠️  Could not extract webhook ID[/yellow]")
            console.print("Command output:")
            console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error creating webhook:[/red] {e.stdout}")

        if e.stderr and "authentication" in e.stderr.lower():
            console.print("\n[yellow]💡 You need to login to Stripe:[/yellow]")
            console.print("[cyan]stripe login[/cyan]")
        elif e.stderr and "url" in e.stderr.lower():
            console.print("\n[yellow]💡 Check your webhook URL:[/yellow]")
            console.print(f"Current URL: {url}")
            console.print("Make sure BASE_URL is correctly configured in your .env")
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")


async def get_webhook_secret(webhook_id: str) -> None:
    """Get the signing secret of a webhook"""

    try:
        subprocess.run(
            ["stripe", "webhooks", "retrieve", webhook_id], 
            check=True, capture_output=True, text=True
        )

        console.print("\n[yellow]🔑 To get the signing secret:[/yellow]")
        console.print(f"1. Go to https://dashboard.stripe.com/test/webhooks/{webhook_id}")
        console.print("2. Click 'Reveal' in the 'Signing secret' section")
        console.print("3. Copy the secret that starts with 'whsec_'")
        console.print("4. Add it to your .env: [cyan]STRIPE_WEBHOOK_SECRET=whsec_...[/cyan]")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error retrieving webhook: {e.stderr}[/red]")
