import cli
import os
import sys
import subprocess


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@cli.argument('args', nargs=-1, type=cli.UNPROCESSED)
def test(args):
    """Run the tests using pytest

    All arguments and options are passed directly to Pytest.

    Examples:

        kt test -v # Run tests with verbose output

        kt test tests/test_main.py # Run specific test file

        kt test -k "test_name" # Run tests matching the given name
    """
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env = os.environ.copy()
    env['PYTHONPATH'] = 'server'

    pytest_cmd = [sys.executable, '-m', 'pytest', 'tests'] + list(args)
    result = subprocess.run(pytest_cmd, env=env, cwd=root)

    sys.exit(result.returncode)
