def test_remesh_task():
    from pytest import raises
    from cloudvolume.exceptions import InfoUnavailableError
    from app.meshing.remesh_pending import remesh_task
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    from .. import TEST_DATASETS_PATH

    with raises((ChunkedGraphError, InfoUnavailableError)):
        remesh_task(TEST_DATASETS_PATH)
