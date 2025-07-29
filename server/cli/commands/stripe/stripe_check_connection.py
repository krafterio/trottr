import cli
from rich.console import Console

from cli.commands.stripe import stripe
from core.app import CliApp

console = Console()


@stripe.command(name="check-connection")
@cli.pass_app
async def check_connection(app: CliApp) -> None:
    """Check connection with Stripe"""
    try:
        console.print("Check connection with Stripe")

        import stripe
        from core.config import get_settings

        settings = get_settings()
        stripe.api_key = settings.stripe_secret_key

        products = stripe.Product.list(limit=1)

        console.print("[green]Successfully connected to Stripe[/green]")
        console.print(f"Number of products: {len(products.data)}")
    except Exception as e:
        console.print(f"[red]Error connecting to Stripe:[/red] {e}")
