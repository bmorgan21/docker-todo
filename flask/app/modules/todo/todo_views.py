from ct_core_api.common import app_utils

from flask import Blueprint
from flask_login import login_required

bp = Blueprint('view.todo', __name__)


@bp.route("/")
@app_utils.template()
@login_required
def index():
    pass
