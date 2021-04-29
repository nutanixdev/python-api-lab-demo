from lab.forms import clusterForm

from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/")
def index():
    # make sure we are using the form that's been generated in forms.py
    form = clusterForm()
    return render_template("index.html", form=form)
