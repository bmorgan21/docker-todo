from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('todo_app.settings')
app.config.from_pyfile('settings.cfg', silent=True)

from todo_app.views import todo

app.register_blueprint(todo.mod)

# import commands
import todo_app.commands  # noqa
