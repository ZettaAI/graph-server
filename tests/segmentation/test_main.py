from pytest import raises

from ..test_main import client


def test_home():
    response = client.get("/segmentation")
    assert response.status_code == 200
    assert response.json().get("version") != None


def test_info():
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get("/segmentation/table/test/info")
        assert response.status_code == 500
