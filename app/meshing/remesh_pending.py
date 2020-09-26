from pychunkedgraph.graph import ChunkedGraph
from .utils import remesh_pending
from ..utils import get_datasets
from ..utils import DATASETS_PATH


def remesh_task(glob_path: str) -> None:
    from pychunkedgraph.graph.exceptions import ChunkedGraphError

    for dataset in get_datasets(glob_path=glob_path):
        graph_id, client_info = dataset
        try:
            cg = ChunkedGraph(graph_id=graph_id, client_info=client_info)
        except Exception as e:
            raise ChunkedGraphError(e)
        remesh_pending(cg)


if __name__ == "__main__":
    remesh_task(DATASETS_PATH)
