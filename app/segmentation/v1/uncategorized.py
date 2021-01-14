from fastapi import APIRouter
from ...utils import get_cg
from .edits_helpers import _process_node_info

router = APIRouter()


@router.post("/{graph_id}/graph/find_path")
async def find_path(
    request: Request,
    graph_id: str,
    int64_as_str: Optional[bool] = False,
    precision_mode: Optional[bool] = True,
):
    from pychunkedgraph.graph.analysis import pathing
    from pychunkedgraph.meshing import mesh_analysis

    cg = copy(get_cg(graph_id))
    nodes = loads(await request.body())
    assert len(nodes) == 2
    supervoxel_ids, _ = _process_node_info(cg, nodes)
    source_sv_id = supervoxel_ids[0]
    target_sv_id = supervoxel_ids[1]
    source_l2_id = cg.get_parent(source_supervoxel_id)
    target_l2_id = cg.get_parent(target_supervoxel_id)

    l2_path = pathing.find_l2_shortest_path(cg, source_l2_id, target_l2_id)
    if precision_mode:
        centroids, failed_l2_ids = mesh_analysis.compute_mesh_centroids_of_l2_ids(
            cg, l2_path, flatten=True
        )
        return {
            "centroids_list": centroids,
            "failed_l2_ids": failed_l2_ids,
            "l2_path": l2_path,
        }
    else:
        centroids = pathing.compute_rough_coordinate_path(cg, l2_path)
        return {"centroids_list": centroids, "failed_l2_ids": [], "l2_path": l2_path}


# ### CONTACT SITES --------------------------------------------------------------


# @bp.route("/table/<table_id>/node/<node_id>/contact_sites", methods=["GET"])
# @auth_requires_permission("view")
# def handle_contact_sites(table_id, node_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     contact_sites, contact_site_metadata = common.handle_contact_sites(
#         table_id, node_id
#     )
#     resp = {
#         "contact_sites": contact_sites,
#         "contact_site_metadata": contact_site_metadata,
#     }
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# @bp.route("/table/<table_id>/node/contact_sites_pair/<first_node_id>/<second_node_id>", methods=["GET"])
# @auth_requires_permission("view")
# def handle_pairwise_contact_sites(table_id, first_node_id, second_node_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     contact_sites, contact_site_metadata = common.handle_pairwise_contact_sites(
#         table_id, first_node_id, second_node_id
#     )
#     resp = {
#         "contact_sites": contact_sites,
#         "contact_site_metadata": contact_site_metadata,
#     }
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)

# ### FIND PATH ------------------------------------------------------------------


# @bp.route("/table/<table_id>/graph/find_path", methods=["POST"])
# @auth_requires_permission("view")
# def find_path(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     precision_mode = request.args.get("precision_mode", default=True, type=toboolean)
#     find_path_result = common.handle_find_path(table_id, precision_mode)
#     return jsonify_with_kwargs(find_path_result, int64_as_str=int64_as_str)


# ### IS LATEST ROOTS --------------------------------------------------------------

# @bp.route("/table/<table_id>/is_latest_roots", methods=["POST"])
# @auth_requires_permission("view")
# def handle_is_latest_roots(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     is_latest_roots = common.handle_is_latest_roots(table_id, is_binary=False)
#     resp = {"is_latest": is_latest_roots}

#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)


# ## Lookup root id from coordinate -----------------------------------------------

# @bp.route("/table/<table_id>/roots_from_coords", methods=["POST"])
# @auth_requires_permission("view")
# def handle_roots_from_coords(table_id):
#     int64_as_str = request.args.get("int64_as_str", default=False, type=toboolean)
#     resp = common.handle_roots_from_coord(table_id)
#     return jsonify_with_kwargs(resp, int64_as_str=int64_as_str)