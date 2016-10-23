from flask import Flask

from todo_app.extensions.login import login_manager
from todo_app.models import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('todo_app.settings')
app.config.from_pyfile('settings.cfg', silent=True)

db.init_app(app)
login_manager.init_app(app)


###
# Register API endpoints
##
from todo_app.apis import bp as api_bp

app.register_blueprint(api_bp, url_prefix='/api')


###
# Register View endpoints
##
from todo_app.views import auth as view_auth
from todo_app.views import todo as view_todo

app.register_blueprint(view_auth.bp, url_prefix='/auth')
app.register_blueprint(view_todo.bp)


###
# Register Commands
##
import todo_app.commands  # noqa
