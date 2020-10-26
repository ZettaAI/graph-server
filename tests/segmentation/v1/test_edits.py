from pytest import raises

from ...test_main import client


def test_merge():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/merge"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_split():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/split"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_split_preview():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/graph/split_preview"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_undo():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/undo"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_redo():
    from starlette.status import HTTP_405_METHOD_NOT_ALLOWED
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    PATH = "/segmentation/api/v1/table/test/redo"
    response = client.get(PATH)
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

    with raises(ChunkedGraphError):
        response = client.post(PATH, json=[1, 2])
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
