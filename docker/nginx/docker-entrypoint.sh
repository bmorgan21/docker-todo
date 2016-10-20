#!/bin/bash
set -eo pipefail

if [ "$1" = 'nginx' ]; then

	UWSGI_PROXY_FILE=/etc/nginx/conf.d/uwsgi_proxy.conf

	# shellcheck disable=SC2153
	if [ ! -f "$UWSGI_PROXY_FILE" ] && [ -n "$UWSGI_UPSTREAM_HOST" ]; then

		echo 'NGinx creating uwsgi proxy file'

		if [ -z "$SERVER_NAME" ]; then
			SERVER_NAME=_
		fi

		if [ -z "$UWSGI_UPSTREAM_PORT" ]; then
			UWSGI_UPSTREAM_PORT=3031
		fi

		cat <<- EOF > "$UWSGI_PROXY_FILE"

			server {
			  listen       80 default_server;
			  server_name  $SERVER_NAME;

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

		if [ -z "$SERVER_NAME" ]; then
			SERVER_NAME=_
		fi

		if [ -z "$HTTP_UPSTREAM_PORT" ]; then
			HTTP_UPSTREAM_PORT=80
		fi

		cat <<- EOF > "$HTTP_PROXY_FILE"

			server {
			  listen       80 default_server;
			  server_name  $SERVER_NAME;

			  location @upstream {
			    internal;

			    proxy_pass  $HTTP_UPSTREAM_HOST:$HTTP_UPSTREAM_PORT;
			  }

			  location / {
			    try_files \$uri @upstream;
			  }
			}

EOF

	fi

    echo
    echo 'Nginx init process done. Ready for start up.'
    echo

fi

exec "$@"
