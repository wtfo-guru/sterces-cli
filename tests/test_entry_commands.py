"""Tests module test_entry_commands for app package sterces-cli."""

from datetime import timezone

import testfixtures
from sterces.foos import str_to_date

from sterces_cli import cli

EG_HELP = """Usage: cli entry [OPTIONS] COMMAND [ARGS]...

  Command group for entry management.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add or update an entry.
  dump    Dump specified entry or all entries if path not specified.
  remove  Remove specified entry.
  show    Show specified entry or all entries if path not specified.
  update  Update specified attributes of entry.
"""

ADD_HELP = """Usage: cli entry add [OPTIONS]

  Add or update an entry.

Options:
  -e, --expires TEXT   specify expire date/time
  -n, --notes TEXT     specify notes
  -o, --otp TEXT       specify notes
  -p, --password TEXT  specify password
  -P, --path TEXT      specify path of entry
  -T, --tags TEXT      specify tags
  -u, --username TEXT  specify username
  --url TEXT           specify url
  -h, --help           Show this message and exit.
"""
ENTRY_TEST_UNO = "/test/test1"


def base_args(dbx: str, pfn: str, cmd: str) -> list[str]:
    """Return base args."""
    return [
        "--db",
        dbx,
        "--passphrase-file",
        pfn,
        "--no-warn",
        "--verbose",
        "entry",
        cmd,
    ]


def base_args_path(dbx, pfn, cmd, path) -> list[str]:
    """Return base args with path."""
    cmd_args = base_args(dbx, pfn, cmd)
    cmd_args.extend(["--path", path])
    return cmd_args


def test_entry_group_help(cli_runner) -> None:
    """Test entry group help."""
    test_result = cli_runner.invoke(
        cli.cli, ["entry", "-h"]
    )  # verifies the short context
    assert test_result.exit_code == 0
    assert not test_result.exception
    testfixtures.compare(EG_HELP, test_result.output)


def test_entry_add(cli_runner, sdbx: str, ppfn: str, expiry: str):
    """Test group add."""
    cmd_args = base_args_path(sdbx, ppfn, "add", ENTRY_TEST_UNO)
    cmd_args.extend(["-p", "passw0rd", "--expires", expiry])
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code == 0
    assert not fruit.exception
    dt = str_to_date(expiry).astimezone(timezone.utc)  # type: ignore [union-attr]
    md = dt.strftime("%Y-%m-%d %H:%M:%S")
    match: str = (
        "'path': ['test', 'test1'], 'title': 'test1', 'username': 'undef', 'password': '********', 'expiry': '{0}'".format(
            md
        )
    )
    assert match in fruit.output


def test_entry_add_dup(cli_runner, sdbx: str, ppfn: str, expiry: str):
    """Test group add."""
    cmd_args = base_args_path(sdbx, ppfn, "add", ENTRY_TEST_UNO)
    cmd_args.extend(["-p", "passw0rd", "--expires", expiry])
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code != 0
    assert "Entry /test/test1 already exists" in fruit.output


def test_entry_update_username(cli_runner, sdbx: str, ppfn: str, expiry: str):
    """Test group add."""
    cmd_args = base_args_path(sdbx, ppfn, "update", ENTRY_TEST_UNO)
    cmd_args.extend(["-a", "username", "-u", "joeblow"])
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code == 0
    assert not fruit.exception
    dt = str_to_date(expiry).astimezone(timezone.utc)  # type: ignore [union-attr]
    md = dt.strftime("%Y-%m-%d %H:%M:%S")
    match: str = (
        "'path': ['test', 'test1'], 'title': 'test1', 'username': 'joeblow', 'password': '********', 'expiry': '{0}'".format(
            md
        )
    )
    assert match in fruit.output


def test_entry_show_one(cli_runner, sdbx: str, ppfn: str, expiry: str):
    """Test group add."""
    cmd_args = base_args(sdbx, ppfn, "show")
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code == 0
    assert not fruit.exception
    dt = str_to_date(expiry).astimezone(timezone.utc)  # type: ignore [union-attr]
    md = dt.strftime("%Y-%m-%d %H:%M:%S")
    match: str = (
        "'path': ['test', 'test1'], 'title': 'test1', 'username': 'joeblow', 'password': '********', 'expiry': '{0}'".format(
            md
        )
    )
    assert match in fruit.output


def test_entry_remove(cli_runner, sdbx: str, ppfn: str):
    """Test group add."""
    cmd_args = base_args_path(sdbx, ppfn, "remove", ENTRY_TEST_UNO)
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code == 0
    assert not fruit.exception
    match = "Entry {0} has been removed".format(ENTRY_TEST_UNO)
    assert match in fruit.output


def test_entry_show_none(cli_runner, sdbx: str, ppfn: str, expiry: str):
    """Test group add."""
    cmd_args = base_args(sdbx, ppfn, "show")
    fruit = cli_runner.invoke(cli.cli, cmd_args)
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert "No entries found" in fruit.output
