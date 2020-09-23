from app.utils import get_datasets


def test_get_datasets():
    datasets = get_datasets(glob_path="tests/datasets/*.yml")

    assert len(datasets) == 2
    assert type(datasets[0]) == tuple

    dataset1 = datasets[0]
    dataset2 = datasets[1]
    assert dataset1[0] == "test_graph1"
    assert dataset2[0] == "test_graph2"