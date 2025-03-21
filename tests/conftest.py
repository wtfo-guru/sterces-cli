"""Test level module test_cli for app package sterces-cli."""

from datetime import datetime, timezone
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def ppfn():
    """Return name of test cache file."""
    path = Path("/tmp/esarhpssap")
    with open(path, "w") as fd:
        fd.write("492434cfcb0446f7152e34f5e8ba4e0e\n")
    return str(path)


@pytest.fixture(scope="session")
def gdbx():
    """Return path to test group db."""
    path = Path("/tmp/group.kdbx")
    if path.exists():
        path.unlink()
    return str(path)


@pytest.fixture(scope="session")
def expiry():
    """Return a sane expiration date as a string."""
    ts = int(datetime.now(timezone.utc).timestamp())
    ts + 864000  # add 10 days
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%m/%d/%Y %H:%M:%S")


@pytest.fixture(scope="session")
def sdbx():
    """Return path to test entries db."""
    path = Path("/tmp/store.kdbx")
    if path.exists():
        path.unlink()
    return str(path)
