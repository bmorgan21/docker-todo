#!/bin/bash

API_SERVICE_FILE=/www/data/app/services/api-service.js

# shellcheck disable=SC2153
if [ ! -f "$API_SERVICE_FILE" ]; then
	cat <<- EOF > "$API_SERVICE_FILE"
angular.module('todoDocker')
    .factory('Api', function($cookies) {
        return {
            getServer: function() {
                return '$ANGULAR_API_SERVER';
            }
        };
    });
EOF
fi

ANGULARJS_FILE=/etc/nginx/conf.d/angularjs.conf

# shellcheck disable=SC2153
if [ ! -f "$ANGULARJS_FILE" ] && [ -n "$ANGULARJS_ROOT_DIR" ]; then

	echo 'NGinx creating AngularJS file'

	if [ -z "$ANGULARJS_SERVER_NAME" ]; then
		ANGULARJS_SERVER_NAME=_
	fi

	if [ -z "$ANGULARJS_PORT" ]; then
		ANGULARJS_PORT="80 default_server"
	fi

	cat <<- EOF > "$ANGULARJS_FILE"

			server {
			  listen       $ANGULARJS_PORT;
			  server_name  $ANGULARJS_SERVER_NAME;

              location / {
                  root $ANGULARJS_ROOT_DIR/app;
              }

              location /bower_components/ {
                  root $ANGULARJS_ROOT_DIR;
              }
			}
EOF
fi
