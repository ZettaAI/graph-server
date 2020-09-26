from pytest import raises

from ..test_main import client


def test_l2_chunk_children():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get("/segmentation/api/v1/table/test/l2_chunk_children/120")
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_l2_chunk_children_binary():
    from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        response = client.get(
            "/segmentation/api/v1/table/test/l2_chunk_children_binary/120"
        )
        assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
