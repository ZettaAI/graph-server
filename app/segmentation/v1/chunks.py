from typing import Union
from typing import Optional
from time import time
from datetime import datetime

from pytz import UTC
from numpy import ndarray

from . import api
from . import string_array


def _l2_chunk_children(
    graph_id: int, chunk_id: int, timestamp: datetime, flatten: bool = False
) -> Union[ndarray, dict]:
    from numpy import array
    from numpy import uint64
    from pychunkedgraph.graph.attributes import Hierarchy
    from . import get_cg

    cg = get_cg(graph_id)
    chunk_id = uint64(chunk_id)
    chunk_layer = cg.get_chunk_layer(chunk_id)
    assert chunk_layer == 2, f"Chunk layer must be 2, got {chunk_layer}"

    rr_chunk = cg.range_read_chunk(
        chunk_id, properties=Hierarchy.Child, time_stamp=timestamp,
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


@api.get("/table/{graph_id}/l2_chunk_children/{chunk_id}")
async def l2_chunk_children(
    graph_id: str,
    chunk_id: int,
    timestamp: Optional[float] = time(),
    int64_as_str: Optional[bool] = False,
    as_array: Optional[bool] = False,
):
    from pickle import dumps

    children = _l2_chunk_children(
        graph_id,
        chunk_id,
        timestamp=datetime.fromtimestamp(timestamp, UTC),
        flatten=as_array,
    )
    if as_array:
        if int64_as_str:
            return {"l2_chunk_children": string_array(children)}
        return {"l2_chunk_children": children}
    return {"l2_chunk_children": dumps(children)}


@api.get("/table/{graph_id}/l2_chunk_children_binary/{chunk_id}")
async def l2_chunk_children_binary(
    graph_id: str,
    chunk_id: int,
    timestamp: Optional[float] = time(),
    as_array: Optional[bool] = False,
):
    from pickle import dumps

    children = _l2_chunk_children(
        graph_id,
        chunk_id,
        timestamp=datetime.fromtimestamp(timestamp, UTC),
        flatten=as_array,
    )
    if as_array:
        return children.tobytes()
    return dumps(children)

