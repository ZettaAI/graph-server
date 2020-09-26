def test_remesh_task():
    from pytest import raises
    from app.meshing.remesh_pending import remesh_task
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    from .. import TEST_DATASETS_PATH
    from .. import TEST_DATASETS_WRONG_PATH

    remesh_task(TEST_DATASETS_WRONG_PATH)

    with raises(ChunkedGraphError):
        remesh_task(TEST_DATASETS_PATH)
