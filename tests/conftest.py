"""Test level module test_cli for app package sterces-cli."""

from datetime import datetime, timezone
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import Generator

import pytest
from sterces.foos import str_to_date


class TestExpiry:
    """Test expiry date handler class."""

    input: str
    output: str

    def __init__(self) -> None:
        """Construct in/out date strings."""
        ts = int(datetime.now(timezone.utc).timestamp())
        ts + 864000  # add 10 days
        self.input = datetime.fromtimestamp(ts, timezone.utc).strftime(
            "%m/%d/%Y %H:%M:%S"
        )
        dt = str_to_date(self.input)
        if dt is None:
            self.output = "Failed to parse: {0}".format(self.input)
        else:
            dt = dt.astimezone(timezone.utc)
            self.output = dt.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(scope="session")
def t_ppf() -> Generator[str, None, None]:
    """Create a temp directory to house test files."""
    td = mkdtemp()
    fn = "{0}/.ssapeek".format(td)
    # dbf = "{0}/db.kdbx".format(td)
    with open(fn, "w") as fd:
        fd.write("492434cfcb0446f7152e34f5e8ba4e0e\n")

    yield fn

    rmtree(td)


@pytest.fixture(scope="session")
def e_args(t_ppf: str) -> tuple[str, ...]:
    """Return name of test cache file."""
    td = Path(t_ppf).parent
    return (  # noqa: WPS227
        "--db",
        "{0}/edb.kdbx".format(td),
        "--passphrase-file",
        t_ppf,
        "--no-warn",
        "entry",
    )


@pytest.fixture(scope="session")
def g_args(t_ppf: str) -> tuple[str, ...]:
    """Return name of test cache file."""
    td = Path(t_ppf).parent
    return (  # noqa: WPS227
        "--db",
        "{0}/gdb.kdbx".format(td),
        "--passphrase-file",
        t_ppf,
        "--no-warn",
        "group",
    )


@pytest.fixture(scope="session")
def expiry() -> TestExpiry:
    """Return class for in/out expiry comparisons."""
    return TestExpiry()
