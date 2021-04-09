from typing import Optional
from copy import copy
from json import loads
from json import dumps

from fastapi import APIRouter
from fastapi import Request
from ...utils import get_cg
from .edits_helpers import _process_node_info

router = APIRouter()


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

