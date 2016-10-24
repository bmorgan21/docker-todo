from flask import Blueprint, render_template
from todo_app.extensions.principal import admin_permission

bp = Blueprint('view.admin', __name__)


@bp.route("/")
@admin_permission.require(403)
def index():
    return render_template('admin/index.html')
