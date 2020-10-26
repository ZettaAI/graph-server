from pytest import raises

from ..test_main import client


def test_home():
    from starlette.status import HTTP_200_OK

    response = client.get("/segmentation")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("version") != None


def test_info():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    with raises(ChunkedGraphError):
        response = client.get("/segmentation/table/test/info")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR