from todo_app.models import db, Todo


def create(**kwargs):
    todo = Todo(**kwargs)

    db.session.add(todo)

    return todo


def get(id):
    todo = Todo.get(id)
    return todo


def get_all():
    todos = Todo.get_all()
    return todos


def get_all_for_user_id(user_id):
    return Todo.get_all_for_user_id(user_id)


def update(id, d):
    todo = get(id)

    for k, v in d.items():
        setattr(todo, k, v)

    return todo


def delete(id):
    Todo.delete(id)
