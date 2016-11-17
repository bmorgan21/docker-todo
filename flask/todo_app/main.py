#!/usr/bin/env python

from todo_app import factory

app = factory.create_app(__name__)


if __name__ == '__main__':
    from ct_core_api.api.app import runner
    runner.run(app)
