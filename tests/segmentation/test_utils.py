from pytest import raises


def test_get_l2_chunk_children():
    from time import time
    from datetime import datetime
    from pytz import UTC
    from app.segmentation.v1.utils import get_l2_chunk_children
    from pychunkedgraph.graph.exceptions import InternalServerError

    with raises(InternalServerError):
        get_l2_chunk_children(
            "test_graph1", 120, timestamp=datetime.fromtimestamp(time(), UTC)
        )

    with raises(InternalServerError):
        get_l2_chunk_children(
            "test_graph1",
            120,
            timestamp=datetime.fromtimestamp(time(), UTC),
            flatten=True,
        )
