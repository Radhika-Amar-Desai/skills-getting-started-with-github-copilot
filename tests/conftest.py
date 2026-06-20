from fastapi.testclient import TestClient
import copy
import pytest

from src.app import app, activities


@pytest.fixture
def app_client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def activities_snapshot():
    """Snapshot and restore the in-memory `activities` dict for test isolation."""
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)
