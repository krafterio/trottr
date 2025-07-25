import cli
from rich.console import Console

from cli.commands.admin import admin
from core.app import CliApp
from models.user import User

console = Console()


@admin.command()
@cli.argument('email', type=str)
@cli.option('--promote', is_flag=True, help='Promote user to superuser')
@cli.pass_app
async def superuser(app: CliApp, email: str, promote: bool) -> None:
    """Promote or demote a user to superuser"""
    async with app.lifespan():
        try:
            user = await User.query.filter(email = email).first()

            if not user:
                raise Exception(f"User with email {email} not found")

            user.is_superuser = promote
            await user.save()

            action = "promoted" if promote else "demoted"
            console.print(f"[green]Successfully {action} {email} to superuser[/green]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
