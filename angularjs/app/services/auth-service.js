angular.module('todoDocker')
    .factory('Auth', function($cookies) {
        var token = $cookies.get('token');

        return {
            setToken: function(value) {
                token = value;
                $cookies.put('token', token);
            },
            getToken: function() {
                return token;
            }
        };
    });
