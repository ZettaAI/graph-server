from typing import Union
from typing import Optional
from datetime import datetime

from numpy import ndarray


def get_l2_chunk_children(
    graph_id: int, chunk_id: int, timestamp: datetime, flatten: Optional[bool] = False
) -> Union[ndarray, dict]:
    from numpy import array
    from numpy import uint64
    from pychunkedgraph.graph.attributes import Hierarchy
    from ..utils import get_cg

    cg = get_cg(graph_id)
    chunk_id = uint64(chunk_id)
    chunk_layer = cg.get_chunk_layer(chunk_id)
    assert chunk_layer == 2, f"Chunk layer must be 2, got {chunk_layer}"

    rr_chunk = cg.range_read_chunk(
        chunk_id, properties=Hierarchy.Child, time_stamp=timestamp
    )

    if flatten:
        l2_chunk_array = []
        for l2 in rr_chunk:
            svs = rr_chunk[l2][0].value
            for sv in svs:
                l2_chunk_array.extend([l2, sv])
        return array(l2_chunk_array)
    else:
        l2_chunk_dict = {}
        for k in rr_chunk:
            l2_chunk_dict[k] = rr_chunk[k][0].value
        return l2_chunk_dict
