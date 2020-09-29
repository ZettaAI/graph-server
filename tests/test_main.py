from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# TODO fix tests after bigtable emulator is setup
def test_home():
    from starlette.status import HTTP_200_OK

    response = client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("version") != None


from os import environ

import pytest

from .helpers import create_graphs
from .helpers import bigtable_emulator


@pytest.mark.timeout(30)
def test_init():
    from app.utils import CACHE

    CACHE = {}
    graphs = create_graphs()

    for g in graphs:
        print(f"Created graph {g.graph_id}")
        CACHE[g.graph_id] = g
