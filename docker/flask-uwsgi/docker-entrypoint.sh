#!/bin/bash
set -eo pipefail

# if command starts with an option, prepend uwsgi
if [ "${1:0:1}" = '-' ]; then
	set -- uwsgi "$@"
fi

# Drop root privileges if we are running uwsgi
# allow the container to be started with `--user`
if [ "$1" = 'uwsgi' -a "$(id -u)" = '0' ]; then

    if [ ! -f "/tmp/uwsgi_first_run" ]; then

        # Invoke extra commands
        echo
        for f in /docker-entrypoint-init-uwsgi.d/*; do
            case "$f" in
                *.sh)     echo "$0: running $f"; . "$f" ;;
                *)        echo "$0: ignoring $f" ;;
            esac
            echo
        done

        touch "/tmp/uwsgi_first_run"

        echo
        echo 'UWSGI init process done. Ready for start up.'
        echo
    fi

    # If the reload parameter set, make sure to append
    if [ "$UWSGI_PY_AUTO_RELOAD" ]; then
        set -- "$@" --py-autoreload $UWSGI_PY_AUTO_RELOAD
    fi

    # There are some defaults we should set
    if [ -z "$UWSGI_PROJECT_HOME" ]; then
        UWSGI_PROJECT_HOME=/var/code
    fi

    if [ -z "$UWSGI_SERVICE_MODULE" ]; then
        UWSGI_SERVICE_MODULE=app:app
    fi

    if [ -z "$UWSGI_PROCESSES" ]; then
        UWSGI_PROCESSES=4
    fi

    if [ -z "$UWSGI_THREADS" ]; then
        UWSGI_THREADS=10
    fi

    if [ -z "$UWSGI_THREADS_STACKSIZE" ]; then
        UWSGI_THREADS_STACKSIZE=1024
    fi

    if [ -z "$UWSGI_SOCKET_PORT" ]; then
        UWSGI_SOCKET_PORT=3031
    fi

    if [ "$UWSGI_HTTP_PORT" ]; then
        set -- "$@" --http :$UWSGI_HTTP_PORT
    fi

    # Append other required arguments (first non-parameterized, then parameterized for uwsgi, then parameterized for app)
    set -- "$@" --master --max-request 100 --die-on-term --socket :$UWSGI_SOCKET_PORT --stats :1717 --buffer-size 16192 --reload-on-rss=768 --thunder-lock
    set -- "$@" --processes $UWSGI_PROCESSES --threads $UWSGI_THREADS --threads-stacksize $UWSGI_THREADS_STACKSIZE
    set -- "$@" --chdir $UWSGI_PROJECT_HOME --pp $UWSGI_PROJECT_HOME --module $UWSGI_SERVICE_MODULE

    SETTINGS_CFG_FILE=$UWSGI_PROJECT_HOME/instance/settings.cfg

    if [ ! -f $SETTINGS_CFG_FILE ]; then
		echo 'Flask uwsgi creating settings.cfg file'

		cat <<- EOF > "$SETTINGS_CFG_FILE"
TEMPLATES_AUTO_RELOAD = True

SQLALCHEMY_DATABASE_URI = 'mysql://$MYSQL_USER:$MYSQL_PASSWORD@db:3306/$MYSQL_DATABASE'
EOF

    fi

    # Now execute under the uwsgi user
    set -- gosu uwsgi "$@"
fi

exec "$@"
