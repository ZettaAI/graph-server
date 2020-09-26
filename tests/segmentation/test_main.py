from pytest import raises

from ..test_main import client


def test_home():
    from starlette.status import HTTP_200_OK

    response = client.get("/segmentation")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("version") != None


def test_info():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get("/segmentation/table/test/info")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_root():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get("/segmentation/api/v1/table/test/node/123/root")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_roots():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    response = client.get("/segmentation/api/v1/table/test/roots")
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    response = client.post("/segmentation/api/v1/table/test/roots")
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    with raises(InternalServerError):
        response = client.post(
            "/segmentation/api/v1/table/test/roots",
            json=[1, 2, 3],
        )
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_roots_binary():
    from numpy import array
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError
    from pychunkedgraph.graph.utils.basetypes import NODE_ID

    response = client.get("/segmentation/api/v1/table/test/roots_binary")
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(InternalServerError):
        response = client.post(
            "/segmentation/api/v1/table/test/roots_binary",
            data=array([3, 2, 1], dtype=NODE_ID).tobytes(),
        )
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_children():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get("/segmentation/api/v1/table/test/node/123/children")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
