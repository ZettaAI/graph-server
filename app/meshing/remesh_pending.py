from pychunkedgraph.graph import ChunkedGraph
from .utils import remesh_pending
from ..utils import get_datasets


def remesh_task():
    for dataset in get_datasets():
        graph_id, client_info = dataset
        cg = ChunkedGraph(graph_id=graph_id, client_info=client_info)
        remesh_pending(cg)


if __name__ == "__main__":
    remesh_task()
