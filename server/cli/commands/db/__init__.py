import cli

import core.orm.migration # noqa: F401

from cli import register_commands_in_group


@cli.group(name="db")
@cli.pass_app
def db(app: cli.CliApp):
    """Database management commands"""
    app.initialize()


register_commands_in_group("edgy.cli.operations", db)
