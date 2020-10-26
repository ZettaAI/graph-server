from pytest import raises

from ...test_main import client


def test_subgraph():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    with raises(ChunkedGraphError):
        response = client.get("/segmentation/api/v1/table/test/node/123/subgraph")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_leaves():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    with raises(ChunkedGraphError):
        response = client.get("/segmentation/api/v1/table/test/node/123/leaves")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
