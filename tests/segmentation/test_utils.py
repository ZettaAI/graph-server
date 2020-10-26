def test_get_l2_chunk_children():
    from time import time
    from datetime import datetime

    from pytest import raises
    from pytz import UTC
    from pychunkedgraph.graph.exceptions import ChunkedGraphError
    from app.segmentation.utils import get_l2_chunk_children

    with raises(ChunkedGraphError):
        get_l2_chunk_children(
            "test_graph", 120, timestamp=datetime.fromtimestamp(time(), UTC)
        )

    with raises(ChunkedGraphError):
        get_l2_chunk_children(
            "test_graph",
            120,
            timestamp=datetime.fromtimestamp(time(), UTC),
            flatten=True,
        )
