import json
from typing import Optional
from typing import Iterable
from datetime import datetime
from dataclasses import asdict

from pychunkedgraph.graph import ChunkedGraph
from pychunkedgraph.graph.attributes import OperationLogs
from pychunkedgraph.export.models import OperationLog


def _parse_attr(attr, val) -> str:
    from numpy import ndarray

    try:
        if isinstance(val, OperationLogs.StatusCodes):
            return (attr.key, val.value)
        if isinstance(val, ndarray):
            return (attr.key, val.tolist())
        return (attr.key, val)
    except AttributeError:
        return (attr, val)


def get_parsed_logs(
    cg: ChunkedGraph,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> Iterable[OperationLog]:
    """Parse logs for compatibility with destination platform."""
    logs = cg.client.read_log_entries(start_time=start_time, end_time=end_time)
    result = []
    for _id, _log in logs.items():
        log = {"id": int(_id)}
        log["status"] = int(_log.get("operation_status", 0))
        for attr, val in _log.items():
            attr, val = _parse_attr(attr, val)
            try:
                log[attr.decode("utf-8")] = val
            except AttributeError:
                log[attr] = val
        result.append(OperationLog(**log))
    print(f"total raw logs {len(result)}")
    return result

cg = ChunkedGraph(graph_id="vnc1_full_v3align_2")
logs = get_parsed_logs(cg)
logs_ds = [asdict(log) for log in logs]

print(logs_ds[0])

with open("logs.json", "w") as f:
    json.dump(logs_ds, f, indent=2, sort_keys=True, default=str)

