from typing import Optional

from fastapi import APIRouter
from ...utils import get_cg
from ...utils import string_array

router = APIRouter()


@router.get("/{graph_id}/node/{node_id}/contact_sites")
async def root_change_log(
    graph_id: str,
    node_id: int,
    bounds: Optional[str] = "",
    partners: Optional[bool] = True,
):
    from numpy import array
    from numpy import uint64
    from pychunkedgraph.graph.misc import get_contact_sites
    from pychunkedgraph.graph.exceptions import BadRequest

    bbox = None
    if bounds:
        bbox = array([b.split("-") for b in bounds.split("_")], dtype=int).T

    contact_sites, contact_site_metadata = get_contact_sites(
        get_cg(graph_id), uint64(node_id), bounding_box=bbox, compute_partner=partners
    )
    return {
        "contact_sites": contact_sites,
        "contact_site_metadata": contact_site_metadata,
    }


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
