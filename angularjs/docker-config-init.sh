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
