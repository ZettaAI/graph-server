from datetime import datetime

from pychunkedgraph.graph import ChunkedGraph
from pychunkedgraph.graph import segmenthistory

from ...utils import get_cg


class LogEntryWrapper:
    def __init__(self, operation_id: int, log: segmenthistory.LogEntry):
        self.operation_id = operation_id
        self.log = log

    def __str__(self):
        log_str = f"{self.log.user_id},{self.log.log_type},{self.log.root_ids},{self.log.timestamp}"
        return f"{self.operation_id},{log_str}"

    def __iter__(self):
        attrs = [
            self.operation_id,
            self.log.user_id,
            self.log.log_type,
            self.log.root_ids,
            self.log.timestamp,
        ]
        for attr in attrs:
            yield attr


def get_change_log(
    graph_id: str, start_time: float = None, end_time: float = None
) -> segmenthistory.SegmentHistory:
    from pytz import UTC

    start_time = datetime.fromtimestamp(start_time, UTC) if start_time else None
    end_time = datetime.fromtimestamp(end_time, UTC) if end_time else None
    return _read_log_entries(get_cg(graph_id), start_time, end_time)


def _read_log_entries(
    cg: ChunkedGraph,
    start_time: datetime,
    end_time: datetime,
) -> list:
    log_entries = []
    log_rows = cg.client.read_log_entries(start_time=start_time, end_time=end_time)
    for _id in range(cg.client.get_max_operation_id()):
        try:
            log = segmenthistory.LogEntry(log_rows[_id], log_rows[_id]["timestamp"])
            log_entries.append(LogEntryWrapper(_id, log))
        except KeyError:
            continue
    return log_entries


def operation_details(graph_id: str, operation_ids: list) -> dict:
    from pychunkedgraph.graph import attributes
    from pychunkedgraph.export.operation_logs import parse_attr

    log_rows = get_cg(graph_id).client.read_log_entries(operation_ids)

    result = {}
    for k, v in log_rows.items():
        details = {}
        for _k, _v in v.items():
            _k, _v = parse_attr(_k, _v)
            try:
                details[_k.decode("utf-8")] = _v
            except AttributeError:
                details[_k] = _v
        result[int(k)] = details
    return result