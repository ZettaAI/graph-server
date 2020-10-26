def remesh_task(glob_path: str) -> None:
    from pychunkedgraph.graph import ChunkedGraph
    from pychunkedgraph.graph.exceptions import ChunkedGraphError
    from .utils import remesh_pending
    from ..utils import CACHE
    from ..utils import get_datasets

    for dataset in get_datasets(glob_path=glob_path):
        graph_id, client_info = dataset
        try:
            cg = ChunkedGraph(graph_id=graph_id, client_info=client_info)
        except Exception as e:
            raise ChunkedGraphError(e)
        remesh_pending(cg)


if __name__ == "__main__":
    from ..utils import DATASETS_PATH

    remesh_task(DATASETS_PATH)
