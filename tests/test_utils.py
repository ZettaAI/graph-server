from pytest import raises

from . import TEST_DATASETS_PATH


def test_get_datasets():
    from app.utils import get_datasets

    datasets = get_datasets(TEST_DATASETS_PATH)

    assert len(datasets) == 2
    assert type(datasets[0]) == tuple

    dataset1_name, dataset1_clientinfo = datasets[0]
    dataset2_name, dataset2_clientinfo = datasets[1]
    assert dataset1_name == "test_graph1"
    assert dataset2_name == "test_graph2"

    assert dataset1_clientinfo.TYPE == "bigtable"
    assert dataset1_clientinfo.CONFIG.PROJECT == "IGNORE_ENVIRONMENT_PROJECT"

    assert dataset1_clientinfo.CONFIG.ADMIN == True
    assert dataset2_clientinfo.CONFIG.ADMIN == False


def test_get_cg():
    from pychunkedgraph.graph import ChunkedGraph
    from app.utils import get_cg

    with raises(Exception):
        get_cg("test_graph1")


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