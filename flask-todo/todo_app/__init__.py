from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('todo_app.settings')
app.config.from_pyfile('settings.cfg', silent=True)

###
# Register API endpoints
##
from todo_app.apis import bp as api_bp

app.register_blueprint(api_bp, url_prefix='/api')


###
# Register View endpoints
##
from todo_app.views import todo as view_todo

app.register_blueprint(view_todo.bp)


###
# Register Commands
##
import todo_app.commands  # noqa
