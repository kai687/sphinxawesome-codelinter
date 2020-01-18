import pytest
from sphinx.testing.path import path

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "example"


def pytest_configure(config):
    """register `sphinx` marker"""

    config.addinivalue_line("markers", "sphinx")
