import os
import subprocess

import pytest
import numpy as np
from google.auth import credentials


class CloudVolumeBounds(object):
    def __init__(self, bounds=[[0, 0, 0], [0, 0, 0]]):
        self._bounds = np.array(bounds)

    @property
    def bounds(self):
        return self._bounds

    def __repr__(self):
        return self.bounds

    def to_list(self):
        return list(np.array(self.bounds).flatten())


class CloudVolumeMock(object):
    def __init__(self):
        self.resolution = np.array([1, 1, 1], dtype=np.int)
        self.bounds = CloudVolumeBounds()


def get_layer_chunk_bounds(n_layers: int, bounds: np.ndarray = np.array([])) -> dict:
    if bounds.size == 0:
        limit = 2 ** (n_layers - 2)
        bounds = np.array([limit, limit, limit])
    layer_bounds_d = {}
    for layer in range(2, n_layers):
        layer_bounds = bounds / (2 ** (layer - 2))
        layer_bounds_d[layer] = np.ceil(layer_bounds).astype(np.int)
    return layer_bounds_d


def setup_emulator_env():
    from google.cloud import bigtable

    bt_env_init = subprocess.run(
        [
            "gcloud",
            "beta",
            "emulators",
            "bigtable",
            "env-init",
        ],
        stdout=subprocess.PIPE,
    )
    os.environ["BIGTABLE_EMULATOR_HOST"] = (
        bt_env_init.stdout.decode("utf-8").strip().split("=")[-1]
    )

    c = bigtable.Client(
        project="IGNORE_ENVIRONMENT_PROJECT",
        credentials=credentials.AnonymousCredentials(),
        admin=True,
    )
    t = c.instance("emulated_instance").table("emulated_table")

    try:
        t.create()
        return True
    except Exception as err:
        print("Bigtable Emulator not yet ready: %s" % err)
        return False


@pytest.fixture(scope="session", autouse=True)
def bigtable_emulator(request):
    from time import sleep
    from signal import SIGTERM

    # Start Emulator
    bigtable_emulator = subprocess.Popen(
        [
            "gcloud",
            "beta",
            "emulators",
            "bigtable",
            "start",
            "--host-port=localhost:8539",
        ],
        preexec_fn=os.setsid,
        stdout=subprocess.PIPE,
    )

    # Wait for Emulator to start up
    print("Waiting for BigTables Emulator to start up...", end="")
    retries = 5
    while retries > 0:
        if setup_emulator_env() is True:
            break
        else:
            retries -= 1
            sleep(5)

    if retries == 0:
        print("\nCouldn't start Bigtable Emulator.")
        exit(1)

    # Setup Emulator-Finalizer
    def fin():
        os.killpg(os.getpgid(bigtable_emulator.pid), SIGTERM)
        bigtable_emulator.wait()

    request.addfinalizer(fin)


def create_graphs():
    from datetime import timedelta

    from pychunkedgraph.graph.chunkedgraph import ChunkedGraph
    from pychunkedgraph.graph.edges import Edges
    from pychunkedgraph.ingest.utils import bootstrap

    n_layers = 10
    bounds = np.array([])

    config = {
        "data_source": {
            "EDGES": "gs://graph/test_graph1/edges",
            "COMPONENTS": "gs://graph/test_graph1/components",
            "WATERSHED": "gs://watershed/test_data1",
        },
        "graph_config": {
            "CHUNK_SIZE": [512, 512, 64],
            "FANOUT": 2,
            "SPATIAL_BITS": 10,
            "ID_PREFIX": "",
            "ROOT_LOCK_EXPIRY": timedelta(seconds=5),
        },
        "backend_client": {
            "TYPE": "bigtable",
            "CONFIG": {
                "ADMIN": True,
                "READ_ONLY": False,
                "PROJECT": "IGNORE_ENVIRONMENT_PROJECT",
                "INSTANCE": "emulated_instance",
                "CREDENTIALS": credentials.AnonymousCredentials(),
            },
        },
        "ingest_config": {},
    }

    graphs = []

    graph_id = "test_graph1"
    meta, _, client_info = bootstrap(graph_id, config=config)
    graph = ChunkedGraph(graph_id=graph_id, meta=meta, client_info=client_info)
    graph.mock_edges = Edges([], [])
    graph.meta._ws_cv = CloudVolumeMock()
    graph.meta.layer_count = n_layers
    graph.meta.layer_chunk_bounds = get_layer_chunk_bounds(n_layers, bounds=bounds)
    graph.create()
    graphs.append(graph)

    graph_id = "test_graph2"
    meta, _, client_info = bootstrap(graph_id, config=config)
    graph = ChunkedGraph(graph_id=graph_id, meta=meta, client_info=client_info)
    graph.mock_edges = Edges([], [])
    graph.meta._ws_cv = CloudVolumeMock()
    graph.meta.layer_count = n_layers
    graph.meta.layer_chunk_bounds = get_layer_chunk_bounds(n_layers, bounds=bounds)
    graph.create()
    graphs.append(graph)
    return graphs
