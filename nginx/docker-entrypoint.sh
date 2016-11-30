#!/bin/bash
set -eo pipefail

if [ "$1" = 'nginx' ]; then

	UWSGI_PROXY_FILE=/etc/nginx/conf.d/uwsgi_proxy.conf

	# shellcheck disable=SC2153
	if [ ! -f "$UWSGI_PROXY_FILE" ] && [ -n "$UWSGI_UPSTREAM_HOST" ]; then

		echo 'NGinx creating uwsgi proxy file'

		if [ -z "$UWSGI_PROXY_SERVER_NAME" ]; then
			UWSGI_PROXY_SERVER_NAME=_
		fi

		if [ -z "$UWSGI_UPSTREAM_PORT" ]; then
			UWSGI_UPSTREAM_PORT=3031
		fi

	    if [ -z "$UWSGI_PROXY_PORT" ]; then
		    UWSGI_PROXY_PORT = "80 default";
	    fi

		cat <<- EOF > "$UWSGI_PROXY_FILE"

			server {
			  listen       $UWSGI_PROXY_PORT;
			  server_name  $UWSGI_PROXY_SERVER_NAME;

			  location @upstream {
			    internal;

			    include uwsgi_params;
			    uwsgi_pass  $UWSGI_UPSTREAM_HOST:$UWSGI_UPSTREAM_PORT;
			    uwsgi_read_timeout 300;
			  }

			  location / {
			    try_files \$uri @upstream;
			  }
			}

EOF

	fi

	HTTP_PROXY_FILE=/etc/nginx/conf.d/http_proxy.conf

	# shellcheck disable=SC2153
	if [ ! -f "$HTTP_PROXY_FILE" ] && [ -n "$HTTP_UPSTREAM_HOST" ]; then

		echo 'NGinx creating HTTP proxy file'

		if [ -z "$HTTP_PROXY_SERVER_NAME" ]; then
			HTTP_PROXY_SERVER_NAME=_
		fi

		if [ -z "$HTTP_UPSTREAM_PORT" ]; then
			HTTP_UPSTREAM_PORT=80
		fi

		if [ -z "$HTTP_PROXY_PORT" ]; then
			HTTP_PROXY_PORT="80  default_server"
		fi

		cat <<- EOF > "$HTTP_PROXY_FILE"

			server {
			  listen       $HTTP_PROXY_PORT;
			  server_name  $HTTP_PROXY_SERVER_NAME;

			  location @upstream {
			    internal;

                proxy_set_header X-Real-IP \$remote_addr;
                proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Host \$http_host;
                proxy_set_header Host \$http_host;

			    proxy_pass  $HTTP_UPSTREAM_HOST:$HTTP_UPSTREAM_PORT;
			  }

			  location / {
			    try_files \$uri @upstream;
			  }
			}

EOF

	fi

	STATIC_FILE=/etc/nginx/conf.d/static.conf

	# shellcheck disable=SC2153
	if [ ! -f "$STATIC_FILE" ] && [ -n "$STATIC_ROOT_DIR" ]; then

		echo 'NGinx creating Static file'

		if [ -z "$STATIC_SERVER_NAME" ]; then
			STATIC_SERVER_NAME=_
		fi

		if [ -z "$STATIC_PORT" ]; then
			STATIC_PORT="80 default_server"
		fi

		cat <<- EOF > "$STATIC_FILE"

			server {
			  listen       $STATIC_PORT;
			  server_name  $STATIC_SERVER_NAME;

              root $STATIC_ROOT_DIR;
			}

EOF

	fi

    if [ ! -f "/tmp/nginx_first_run" ]; then

        # Invoke extra commands
        echo
        for f in /docker-entrypoint-init-nginx.d/*; do
            case "$f" in
                *.sh)     echo "$0: running $f"; . "$f" ;;
                *)        echo "$0: ignoring $f" ;;
            esac
            echo
        done

        touch "/tmp/nginx_first_run"

        echo
        echo 'UWSGI init process done. Ready for start up.'
        echo
    fi

    echo
    echo 'Nginx init process done. Ready for start up.'
    echo

fi

exec "$@"
