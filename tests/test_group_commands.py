"""Tests module test_group_commands for app package sterces-cli."""

import testfixtures

from sterces_cli import cli

GG_HELP = """Usage: cli group [OPTIONS] COMMAND [ARGS]...

  Command group for group management.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add group and show.
  remove  Remove group and show.
  show    Show groups.
"""


def test_group_group_help(cli_runner) -> None:
    """Test group group help."""
    test_result = cli_runner.invoke(
        cli.cli, ["group", "-h"]
    )  # verifies the short context
    assert test_result.exit_code == 0
    assert not test_result.exception
    testfixtures.compare(GG_HELP, test_result.output)


def test_group_add(cli_runner, gdbx: str, ppfn: str):
    """Test group add."""
    fruit = cli_runner.invoke(
        cli.cli,
        [
            "--db",
            gdbx,
            "--passphrase-file",
            ppfn,
            "--no-warn",
            "group",
            "add",
            "--path",
            "/internet/email/gmail/qs5779/",
            "--no-quiet",
        ],
    )
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert (
        '[Group: "", Group: "internet", Group: "internet/email", Group: "internet/email/gmail", Group: "internet/email/gmail/qs5779"]'
        in fruit.output
    )


def test_group_remove(cli_runner, gdbx: str, ppfn: str):
    """Test group remove."""
    fruit = cli_runner.invoke(
        cli.cli,
        [
            "--db",
            gdbx,
            "--passphrase-file",
            ppfn,
            "--no-warn",
            "group",
            "remove",
            "--path",
            "/internet",
            "--no-quiet",
        ],
    )
    assert fruit.exit_code == 0
    assert not fruit.exception
    assert '[Group: ""]' in fruit.output
