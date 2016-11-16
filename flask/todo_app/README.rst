Flask Todo App
##############

Quick Start
===========

Set environment vars for the Flask application::

    export FLASK_APP=app/main.py
    export FLASK_DEBUG=1
    export FLASK_CONFIG=development

Install runtime dependencies::

    pip install -r requirements.txt

View application information::

    flask app

Run the application::

    flask run

Setup for test runners::

    pip install -r tests/requirements.txt

Run tests::

    pytest
