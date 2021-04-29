import os
import json
import base64
from datetime import datetime
from datetime import timedelta
import time
import urllib3

from flask import (
    Blueprint,
    request,
    jsonify,
)

from .util import apiclient

bp = Blueprint("ajax", __name__, url_prefix="/ajax")

"""
disable insecure connection warnings
please be advised and aware of the implications of doing this
in a production environment!
"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


"""
get the form POST data provided by the user
"""


def get_form():
    global form_data
    global cvmAddress
    global username
    global password
    global entity
    form_data = request.form
    cvmAddress = form_data["_cvmAddress"]
    username = form_data["_username"]
    password = form_data["_password"]
    entity = form_data["_entity"]


"""
load the default layout at app startup
"""


@bp.route("/load-layout", methods=["POST"])
def load_layout():
    site_root = os.path.realpath(os.path.dirname(__file__))
    layout_path = "static/layouts"
    dashboard_file = "dashboard.json"
    with open(f"{site_root}/{layout_path}/{dashboard_file}", "r") as f:
        raw_json = json.loads(f.read())
        return base64.b64decode(raw_json["layout"]).decode("utf-8")


"""
connect to prism central and collect details about a specific type of entity
"""


@bp.route("/pc-list-entities", methods=["POST"])
def pc_list_entities():
    # get the request's POST data
    get_form()
    client = apiclient.ApiClient(
        method="post",
        cluster_ip=cvmAddress,
        request=f"{entity}s/list",
        entity=entity,
        body=f'{{"kind": "{entity}"}}',
        username=username,
        password=password,
    )
    results = client.get_info()
    return jsonify(results)


"""
get storage performance stats for the first storage container in a cluster
"""


@bp.route("/storage-performance", methods=["POST"])
def storage_performance():
    # get the request's POST data
    get_form()

    # get the current time then substract 4 hours
    # this is used for the storage performance chart
    endTime = datetime.now()
    delta = timedelta(hours=-4)
    startTime = endTime + delta
    endTime = round(time.mktime(endTime.timetuple()) * 1000 * 1000)
    startTime = round(time.mktime(startTime.timetuple()) * 1000 * 1000)

    # first, get the external IP address of the first cluster registered to this Prism Central instance
    entity = "cluster"
    client = apiclient.ApiClient(
        method="post",
        cluster_ip=cvmAddress,
        request=f"{entity}s/list",
        entity=entity,
        body=f'{{"kind": "{entity}"}}',
        username=username,
        password=password,
    )
    cluster_ip = client.get_info()["entities"][0]["status"]["resources"]["network"][
        "external_ip"
    ]

    # next, get the UUID of the first storage container in the cluster found in our previous request
    entity = "storage_containers"
    client = apiclient.ApiClient(
        method="get",
        cluster_ip=cluster_ip,
        request=entity,
        entity="",
        body="",
        username=username,
        password=password,
        version="v2.0",
    )
    storage_container_uuid = client.get_info()["entities"][0]["id"]

    # finally, get the performance stats for the storage container found in our previous request
    entity = "storage_containers"
    full_request = f"storage_containers/{storage_container_uuid}/stats/?metrics=controller_avg_io_latency_usecs&start_time_in_usecs={startTime}&end_time_in_usecs={endTime}"
    client = apiclient.ApiClient(
        method="get",
        cluster_ip=cluster_ip,
        request=full_request,
        entity="",
        body="",
        username=username,
        password=password,
        version="v2.0",
    )
    stats = client.get_info()

    # return the JSON array containing storage container performance info for the last 4 hours
    return jsonify(stats)
