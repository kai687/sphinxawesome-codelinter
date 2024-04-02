"""Common configurations and fixtures for Pytest."""

from typing import Any

import pytest
from _pytest.config import Config
from sphinx import version_info

if version_info >= (7, 2):
    from pathlib import Path
else:
    from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> Any:
    """Root directory for test files."""
    if version_info >= (7, 2):
        return Path(__file__).parent.absolute()
    else:
        return path(__file__).parent.abspath()


def pytest_configure(config: Config) -> None:
    """Register `sphinx` marker with Pytest."""
    config.addinivalue_line("markers", "sphinx")
