from todo_app.models import db, Todo


def transform_data(d):
    result = {}

    map = {
        'id': 'id',
        'title': 'name',
        'completed': 'is_complete'
    }

    for k, v in d.items():
        if k in map:
            result[map[k]] = v

    return result


def create_from_dict(d):
    todo = Todo(**transform_data(d))

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

    d = transform_data(d)

    for k, v in d.items():
        setattr(todo, k, v)

    return todo


def delete(id):
    Todo.delete(id)
