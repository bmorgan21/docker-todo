from flask import Blueprint, render_template

mod = Blueprint('todo', __name__)


@mod.route("/")
def index():
    return render_template('index.html')
