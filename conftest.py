import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner(mix_stderr=False)
