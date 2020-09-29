from pytest import raises

from . import TEST_DATASETS_PATH


def test_get_datasets():
    from app.utils import get_datasets

    datasets = get_datasets(TEST_DATASETS_PATH)

    assert len(datasets) == 1
    assert type(datasets[0]) == tuple

    dataset_name, dataset_clientinfo = datasets[0]
    assert dataset_name == "test_graph"

    assert dataset_clientinfo.TYPE == "bigtable"
    assert dataset_clientinfo.CONFIG.PROJECT == "IGNORE_ENVIRONMENT_PROJECT"
    assert dataset_clientinfo.CONFIG.ADMIN == True


def test_get_cg():
    from pychunkedgraph.graph import ChunkedGraph
    from app.utils import get_cg

    with raises(Exception):
        get_cg("test_graph")


def test_string_array():
    import numpy as np
    from pychunkedgraph.graph.utils.basetypes import NODE_ID
    from app.utils import string_array

    a = np.array([1, 2, 3], dtype=NODE_ID)
    a = string_array(a)
    assert a == ["1", "2", "3"]


def test_toboolean():
    from app.utils import toboolean

    with raises(ValueError):
        toboolean(None)

    assert toboolean(0) == False
    assert toboolean(1) == True
    assert toboolean(1.1) == True
    assert toboolean(-1.1) == True

    assert toboolean(True) == True
    assert toboolean("true") == True
    assert toboolean("False") == False