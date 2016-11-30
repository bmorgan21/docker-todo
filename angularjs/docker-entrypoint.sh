#!/bin/bash

if [ "$1" = 'nginx' ]; then
	API_SERVICE_FILE=/www/data/app/services/api-service.js

	# shellcheck disable=SC2153
	if [ ! -f "$API_SERVICE_FILE" ] && [ -n "$ANGULAR_API_SERVER" ]; then
		cat <<- EOF > "$STATIC_FILE"
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
fi
