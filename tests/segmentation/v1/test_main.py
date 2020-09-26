from pytest import raises

from ...test_main import client


def test_root():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    with raises(ChunkedGraphError):
        response = client.get("/segmentation/api/v1/table/test/node/123/root")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_roots():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/roots"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    response = client.post(PATH)
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2, 3])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_roots_binary():
    from numpy import array
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError
    from pychunkedgraph.graph.utils.basetypes import NODE_ID

    PATH = "/segmentation/api/v1/table/test/roots_binary"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, data=array([3, 2, 1], dtype=NODE_ID).tobytes())
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_children():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    with raises(ChunkedGraphError):
        response = client.get("/segmentation/api/v1/table/test/node/123/children")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
