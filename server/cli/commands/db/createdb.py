import cli
from rich.console import Console
from edgy import Database

from cli.commands.db import db
from core.app import CliApp
from sqlalchemy.engine.url import make_url

import sys
import threading

# Monkey-patch to ignore _DeleteDummyThreadOnDel exception at process termination with Python 3.13
_old = threading._DeleteDummyThreadOnDel.__del__ # type: ignore
def _safe_del(self):
    if sys and sys.is_finalizing():
        return
    try:
        _old(self)
    except Exception:
        pass
threading._DeleteDummyThreadOnDel.__del__ = _safe_del # type: ignore


console = Console()


@db.command()
@cli.pass_app
async def createdb(app: CliApp):
    """Create the database"""
    db_url = make_url(app.settings.database_url).set(database="postgres")
    admin_database_url = (
        f"{db_url.drivername}://"
        f"{db_url.username}:{db_url.password}@"
        f"{db_url.host or ''}"
        f"{':' + str(db_url.port) if db_url.port else ''}/"
        f"{db_url.database}"
    )
    dbname = app.settings.db_name

    db_admin = Database(admin_database_url)
    await db_admin.connect()
    result = await db_admin.execute("SELECT 1 FROM pg_database WHERE datname=:dbn", {"dbn": dbname})

    if result:
        console.print(f"[yellow]Database '{dbname}' already exists.[/yellow]")
    else:
        await db_admin.execute(f'CREATE DATABASE "{dbname}"')
        console.print(f"[green]Database '{dbname}' created successfully.[/green]")

    await db_admin.disconnect()
