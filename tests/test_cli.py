"""Tests module test_cli for app package sterces-cli."""

import testfixtures

from sterces_cli import cli
from sterces_cli.constants import VERSION

CLI_HELP = """Usage: cli [OPTIONS] COMMAND [ARGS]...

  Command interface for a KeePass database.

Options:
  -d, --debug                     increment debug level
  -D, --db, --database-file TEXT  keepass db file ( default ~/.sterces/db.kdbx)
  -k, --key-file TEXT             keepass key file (default None)
  -p, --passphrase-file TEXT      passphrase file default ~/.sterces/.ssapeek
  -t, --transformed-key TEXT      keepass transformed key (default None)
  -v, --verbose                   increment verbosity level
  --warn / --no-warn              Warn permissions flag (default True)
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.

Commands:
  entry   Command group for entry management.
  group   Command group for group management.
  lookup  Lookup attribute of an entry.
"""


def test_cli_help(cli_runner):
    """Test help."""
    fruit = cli_runner.invoke(cli.cli)
    assert fruit.exit_code == 0
    assert not fruit.exception
    testfixtures.compare(CLI_HELP, fruit.output)


def test_cli_version(cli_runner):
    """Test help."""
    fruit = cli_runner.invoke(cli.cli, ["--version"])
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert fruit.output.strip() == "cli, version {0}".format(VERSION)
