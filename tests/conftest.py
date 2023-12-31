"""
    Dummy conftest.py for gencli.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()
