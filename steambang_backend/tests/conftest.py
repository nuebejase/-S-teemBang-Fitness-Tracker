import os
import tempfile
from pathlib import Path

import pytest

# Point DB to a temp file before app imports engine
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["STEAMBANG_DATABASE_URL"] = f"sqlite:///{Path(_tmp.name).as_posix()}"
