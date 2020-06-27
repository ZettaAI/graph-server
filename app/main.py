from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    from pychunkedgraph.graph import ChunkedGraph

    cg = ChunkedGraph(graph_id="minnie3_v1")
    return cg.meta.dataset_info


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/table/{table_id}/node/{node_id}/leaves")
def handle_leaves(table_id:str, node_id:str):
    int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
    leaf_ids = common.handle_leaves(table_id, node_id)
    resp = {"leaf_ids": leaf_ids}
    return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)
