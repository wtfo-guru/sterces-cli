"""Top level module cli from package sterces."""

import sys
from pathlib import Path
from typing import NoReturn, Optional

import click
from loguru import logger
from pykeepass.pykeepass import debug_setup
from sterces.db import StercesDatabase

from sterces_cli.constants import CONTEXT_SETTINGS, VERSION
from sterces_cli.entries import commands as entry_actions
from sterces_cli.foos import StrIntStrBool, add_arg_if
from sterces_cli.groups import commands as group_actions

HOME = Path.home()
DEFAULT_PASSWORD_FILE = HOME / ".sterces/.ssapeek"
DEFAULT_DATABASE_FILE = HOME / ".sterces/db.kdbx"


def _configure_logging(verbose: int) -> None:
    logger.remove()  # Remove the default handler.
    if verbose > 0:
        logger.add(sys.stderr, level="INFO")
    else:
        logger.add(sys.stderr, level="WARNING")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option(
    "-D",
    "--db",
    "--database-file",
    default=DEFAULT_DATABASE_FILE,
    help="keepass db file ( default ~/.sterces/db.kdbx)",
)
@click.option(
    "-k",
    "--key-file",
    type=str,
    required=False,
    help="keepass key file (default None)",
)
@click.option(
    "-p",
    "--passphrase-file",
    default=DEFAULT_PASSWORD_FILE,
    help="passphrase file default ~/.sterces/.ssapeek",
)
@click.option(
    "-t",
    "--transformed-key",
    type=str,
    required=False,
    help="keepass transformed key (default None)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="increment verbosity level",
)
@click.option(
    "--warn/--no-warn", default=True, help="Warn permissions flag (default True)"
)
@click.version_option(VERSION)
@click.pass_context
def cli(
    ctx: click.Context,
    debug: int,
    db: str,
    key_file: Optional[str],
    transformed_key: Optional[str],
    passphrase_file: str,
    verbose: int,
    warn: bool,
) -> int:
    """Command interface for a KeePass database."""
    if debug == 0:
        _configure_logging(verbose)
    elif debug > 1:
        debug_setup()
    dbargs: StrIntStrBool = {"debug": debug, "verbose": verbose, "warn": warn}
    add_arg_if(dbargs, "db_fn", db)
    add_arg_if(dbargs, "pwd_fn", passphrase_file)
    add_arg_if(dbargs, "key_fn", key_file)
    add_arg_if(dbargs, "tf_key", transformed_key)
    ctx.obj = StercesDatabase(**dbargs)
    return 0


cli.add_command(group_actions.group)
cli.add_command(entry_actions.entry)


@cli.command()
@click.argument("path", type=str)
@click.argument("attr", default="password")
@click.pass_obj
def lookup(ctx: StercesDatabase, path: str, attr: str) -> NoReturn:
    """Lookup attribute of an entry."""
    sys.exit(ctx.lookup(path, attr))


if __name__ == "__main__":
    sys.exit(cli())  # pragma no cover
