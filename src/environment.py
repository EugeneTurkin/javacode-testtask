"""Module for environment utilities."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Final


def get_env_file() -> Path:
    """Parse and validate environment variable."""
    assert "JAVACODE_ENV" in os.environ, (
        "Set up JAVACODE_ENV environment variable which should be "
        "a path to the directory containing `.env` file relative to `envs/` directory.\n"
        "For example: 'local/test'"
    )

    JAVACODE_ENV: Final = os.environ["JAVACODE_ENV"]
    path = Path(f"envs/{JAVACODE_ENV}/.env")

    assert path.exists(), f"Dotenv file doesn't exist at: {path.absolute()}"
    return path
