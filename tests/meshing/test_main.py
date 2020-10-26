from pytest import raises

from ..test_main import client


def test_home():
    from starlette.status import HTTP_200_OK

    response = client.get("/meshing")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("version") != None
