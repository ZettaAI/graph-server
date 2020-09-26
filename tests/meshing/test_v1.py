from pytest import raises

from ..test_main import client


def test_manifest():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/meshing/api/v1/table/test/manifest/123:0"
    with raises(ChunkedGraphError):
        response = client.get(PATH)
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_remesh():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/meshing/api/v1/table/test/remesh"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
