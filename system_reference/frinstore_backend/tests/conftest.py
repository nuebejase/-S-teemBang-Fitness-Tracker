"""Pytest configuration: isolated SQLite DB before any app imports."""

from __future__ import annotations

import atexit
import os
import tempfile
from pathlib import Path

_fd, _TEST_DB_PATH = tempfile.mkstemp(suffix="_frinstore_pytest.sqlite")
os.close(_fd)
_test_db = Path(_TEST_DB_PATH).resolve()
os.environ["FRINSTORE_DATABASE_URL"] = f"sqlite:///{_test_db.as_posix()}"


def _cleanup_db_file() -> None:
    try:
        _test_db.unlink(missing_ok=True)
    except OSError:
        pass


atexit.register(_cleanup_db_file)
