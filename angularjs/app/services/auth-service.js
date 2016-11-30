angular.module('todoDocker')
    .factory('Auth', function($cookies) {
        var token = $cookies.get('token');
        var auth_mode = 'query';

        return {
            setToken: function(value) {
                token = value;
                $cookies.put('token', token);
            },
            getToken: function() {
                return token;
            },
            getAuthMode: function() {
                return auth_mode;
            }
        };
    });
