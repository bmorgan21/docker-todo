from todo_app.models import db, Todo


def create_from_dict(d):
    todo = Todo(**d.items())

    db.session.add(todo)

    return todo


def get(id):
    todo = Todo.get(id)
    return todo


def get_all():
    todos = Todo.get_all()
    return todos


def update(id, d):
    todo = get(id)

    map = {
        'task': 'name'
    }

    for k, v in d.items():
        if hasattr(todo, k):
            setattr(todo, k, v)
        elif k in map:
            setattr(todo, map[k], v)

    return todo


def delete(id):
    Todo.delete(id)
