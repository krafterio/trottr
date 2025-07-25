import asyncio
import logging
import click
import importlib
import inspect
import pkgutil

from click.decorators import _AnyCallable
from functools import update_wrapper
from typing import Any, Awaitable, Callable, Dict, Type, TypeVar, Union, cast
from typing_extensions import Concatenate, ParamSpec

from core.app import CliApp

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")

# Click Core
from click import Argument as Argument
from click import Context as Context
from click import Parameter as Parameter

# Click Decorators
from click import argument as argument
from click import option as option
from click import confirmation_option as confirmation_option
from click import help_option as help_option
from click import password_option as password_option
from click import version_option as version_option

# Click Exceptions
from click import Abort as Abort
from click import BadArgumentUsage as BadArgumentUsage
from click import BadOptionUsage as BadOptionUsage
from click import BadParameter as BadParameter
from click import ClickException as ClickException
from click import FileError as FileError
from click import MissingParameter as MissingParameter
from click import NoSuchOption as NoSuchOption
from click import UsageError as UsageError

# Click Formatting
from click import HelpFormatter as HelpFormatter
from click import wrap_text as wrap_text

# Click Globals
from click import get_current_context as get_current_context

# Clck Terminal UI
from click import clear as clear
from click import confirm as confirm
from click import echo_via_pager as echo_via_pager
from click import edit as edit
from click import getchar as getchar
from click import launch as launch
from click import pause as pause
from click import progressbar as progressbar
from click import prompt as prompt
from click import secho as secho
from click import style as style
from click import unstyle as unstyle

# Click Types
from click import BOOL as BOOL
from click import Choice as Choice
from click import DateTime as DateTime
from click import File as File
from click import FLOAT as FLOAT
from click import FloatRange as FloatRange
from click import INT as INT
from click import IntRange as IntRange
from click import ParamType as ParamType
from click import Path as Path
from click import STRING as STRING
from click import Tuple as Tuple
from click import UNPROCESSED as UNPROCESSED
from click import UUID as UUID

# Click Utilities
from click import echo as echo
from click import format_filename as format_filename
from click import get_app_dir as get_app_dir
from click import get_binary_stream as get_binary_stream
from click import get_text_stream as get_text_stream
from click import open_file as open_file

logger = logging.getLogger("cli.command")

_cli_groups: Dict[str, click.Group] = {}
_cli_commands: Dict[str, click.Command] = {}


def register_commands_in_group(package_name : str, cli_group: click.Group) -> None:
    """
    Register all CLI commands in the given package in the given CLI group.
    """
    package = importlib.import_module(package_name)

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if not is_pkg:
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if isinstance(obj, click.Command) and not isinstance(obj, click.Group):
                    cli_group.add_command(obj)


def register_cli_commands(cli: click.Group) -> None:
    """
    Register all discovered CLI commands with the main CLI group.
    """
    # Discover all CLI commands
    discover_cli_commands(__name__ + '.commands')

    # Register all CLI groups with their commands
    for group_name, g in _cli_groups.items():
        cli.add_command(g, name=group_name)

    # Register all CLI commands without groups
    for command_name, cmd in _cli_commands.items():
        parent = find_group_name(cli, cmd)

        if parent is None:
            cli.add_command(cmd, name=command_name)


def discover_cli_commands(package_name: str) -> None:
    """
    Discover and register all CLI commands in the given package.
    """
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."

    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, prefix):
        if is_pkg:
            # Recursively discover commands in subpackages
            discover_cli_commands(module_name)
        else:
            # Import the module and register any CLI commands
            # Note: Commands using the decorator pattern are registered automatically
            # when the module is imported
            module = importlib.import_module(module_name)

            # Find and register click.Group objects (from @click.group())
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, click.Group) and obj not in _cli_groups.values():
                    group_name = getattr(obj, 'name', name)
                    _cli_groups[group_name] = obj

                elif (isinstance(obj, click.Command) and not isinstance(obj, click.Group)
                      and obj not in _cli_commands.values()):
                    command_name = getattr(obj, 'name', name)
                    _cli_commands[command_name] = obj


def find_group_name(root_group: click.Group, cmd: click.Command) -> str | None:
    for group_name, group_command in root_group.commands.items():
        if isinstance(group_command, click.Group):
            for group_cmd_name, group_cmd in group_command.commands.items():
                if group_cmd is cmd:
                    return group_command.name

    return None


class Command(click.Command):
    def invoke(self, ctx: Context) -> Any:
        try:
            invoke = super().invoke(ctx)

            if inspect.iscoroutinefunction(self.callback):
                return asyncio.run(invoke)

            return invoke
        except Exception as e:
            logger.error(f"Error in command '{self.name}': {str(e)}")


class Group(click.Group):
    def command(self, *args: Any, **kwargs: Any) -> Union[Callable[[Callable[..., Any]], Command], Command]:
        def decorator(f: Callable[..., Any]) -> Command:
            kwargs.setdefault('cls', Command)

            return cast(Command, super(Group, self).command(*args, **kwargs)(f))

        return decorator


def command(*args, **kwargs):
    kwargs.setdefault('cls', Command)

    return click.command(*args, **kwargs)


def group(*args, **kwargs) -> Union[Group, Callable[[_AnyCallable], Union[Group, Group]]]:
    kwargs.setdefault('cls', Group)

    return click.group(*args, **kwargs)


def pass_context(f: "Callable[Concatenate[Context, P], R]") -> "Callable[P, R]":
    """Marks a callback as wanting to receive the current context
    object as first argument.
    """
    if inspect.iscoroutinefunction(inspect.unwrap(f)):
        async def async_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
            return await f(get_current_context(), *args, **kwargs)
        wrapped_func = async_func
    else:
        def sync_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
            return f(get_current_context(), *args, **kwargs)
        wrapped_func = sync_func

    return cast(Callable[P, R], update_wrapper(wrapped_func, f))


def pass_app(f: "Callable[Concatenate[CliApp, P], R]") -> "Callable[P, R]":
    """Similar to :func:`pass_context`, but only pass the object on the
    context onwards (:attr:`Context.obj`).  This is useful if that object
    represents the state of a nested system.
    """
    if inspect.iscoroutinefunction(inspect.unwrap(f)):
        async def async_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
            return await f(get_current_context().obj, *args, **kwargs)
        wrapped_func = async_func
    else:
        def sync_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
            return f(get_current_context().obj, *args, **kwargs)
        wrapped_func = sync_func

    return cast(Callable[P, R], update_wrapper(wrapped_func, f))


def make_pass_decorator(
    object_type: Type[T], ensure: bool = False
) -> Callable[["Callable[Concatenate[T, P], R]"], "Callable[P, R]"]:
    """Given an object type this creates a decorator that will work
    similar to :func:`pass_obj` but instead of passing the object of the
    current context, it will find the innermost context of type
    :func:`object_type`.

    This generates a decorator that works roughly like this::

        from functools import update_wrapper

        def decorator(f):
            @pass_context
            def new_func(ctx, *args, **kwargs):
                obj = ctx.find_object(object_type)
                return ctx.invoke(f, obj, *args, **kwargs)
            return update_wrapper(new_func, f)
        return decorator

    :param object_type: the type of the object to pass.
    :param ensure: if set to `True`, a new object will be created and
                   remembered on the context if it's not there yet.
    """

    def decorator(f: "Callable[Concatenate[T, P], R]") -> "Callable[P, R]":
        if inspect.iscoroutinefunction(inspect.unwrap(f)):
            async def async_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
                ctx = get_current_context()

                obj: T | None
                if ensure:
                    obj = ctx.ensure_object(object_type)
                else:
                    obj = ctx.find_object(object_type)

                if obj is None:
                    raise RuntimeError(
                        "Managed to invoke callback without a context"
                        f" object of type {object_type.__name__!r}"
                        " existing."
                    )

                return await cast(Awaitable[R], ctx.invoke(f, obj, *args, **kwargs))
            wrapped_func = async_func
        else:
            def sync_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
                ctx = get_current_context()

                obj: T | None
                if ensure:
                    obj = ctx.ensure_object(object_type)
                else:
                    obj = ctx.find_object(object_type)

                if obj is None:
                    raise RuntimeError(
                        "Managed to invoke callback without a context"
                        f" object of type {object_type.__name__!r}"
                        " existing."
                    )

                return ctx.invoke(f, obj, *args, **kwargs)
            wrapped_func = sync_func

        return cast(Callable[P, R], update_wrapper(wrapped_func, f))

    return decorator


def pass_meta_key(
    key: str, *, doc_description: str | None = None
) -> "Callable[[Callable[Concatenate[Any, P], R]], Callable[P, R]]":
    """Create a decorator that passes a key from
    :attr:`click.Context.meta` as the first argument to the decorated
    function.

    :param key: Key in ``Context.meta`` to pass.
    :param doc_description: Description of the object being passed,
        inserted into the decorator's docstring. Defaults to "the 'key'
        key from Context.meta".

    .. versionadded:: 8.0
    """

    def decorator(f: "Callable[Concatenate[Any, P], R]") -> "Callable[P, R]":
        if inspect.iscoroutinefunction(inspect.unwrap(f)):
            async def async_func(*args: "P.args", **kwargs: "P.kwargs") -> R:
                ctx = get_current_context()
                obj = ctx.meta[key]
                return await cast(Awaitable[R], ctx.invoke(f, obj, *args, **kwargs))
            wrapped_func = async_func
        else:
            def sync_func(*args: "P.args", **kwargs: "P.kwargs") -> R:
                ctx = get_current_context()
                obj = ctx.meta[key]
                return ctx.invoke(f, obj, *args, **kwargs)
            wrapped_func = sync_func

        return cast(Callable[P, R], update_wrapper(wrapped_func, f))

    if doc_description is None:
        doc_description = f"the {key!r} key from :attr:`click.Context.meta`"

    decorator.__doc__ = (
        f"Decorator that passes {doc_description} as the first argument"
        " to the decorated function."
    )
    return decorator


__all__ = [
    # Click Core
    "Argument",
    "Context",
    "Parameter",
    # Click Decorators
    "argument",
    "option",
    "confirmation_option",
    "help_option",
    "password_option",
    "version_option",
    # Click Exceptions
    "Abort",
    "BadArgumentUsage",
    "BadOptionUsage",
    "BadParameter",
    "ClickException",
    "FileError",
    "MissingParameter",
    "NoSuchOption",
    "UsageError",
    # Click Formatting
    "HelpFormatter",
    "wrap_text",
    # Click Globals
    "get_current_context",
    # Click Terminal UI
    "clear",
    "confirm",
    "echo_via_pager",
    "edit",
    "getchar",
    "launch",
    "pause",
    "progressbar",
    "prompt",
    "secho",
    "style",
    "unstyle",
    # Click Types
    "BOOL",
    "Choice",
    "DateTime",
    "File",
    "FLOAT",
    "FloatRange",
    "INT",
    "IntRange",
    "ParamType",
    "Path",
    "STRING",
    "Tuple",
    "UNPROCESSED",
    "UUID",
    # Click Utilities
    "echo",
    "format_filename",
    "get_app_dir",
    "get_binary_stream",
    "get_text_stream",
    "open_file",
    # Custom
    "Command",
    "Group",
    "command",
    "group",
    "pass_context",
    "pass_app",
    "make_pass_decorator",
    "pass_meta_key",
    "register_cli_commands",
    "register_commands_in_group",
    "find_group_name",
    "discover_cli_commands",
]
