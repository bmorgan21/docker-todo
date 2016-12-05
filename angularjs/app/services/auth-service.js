angular.module('todoDocker')
    .factory('Auth', function($cookies) {
        var observerCallbacks = [];

        var notifyObservers = function(name, value) {
            angular.forEach(observerCallbacks, function(d){
                if (d.name == name) {
                    d.func(value);
                }
            });
        };

        var setCookie = function(name, value) {
            if (value) {
                $cookies.put(name, value);
            } else {
                $cookies.remove(name);
            }
        };

        var userId = $cookies.get('userId');
        var token = $cookies.get('token');
        var auth_mode = 'query';

        notifyObservers('userId', userId);
        notifyObservers('token', token);

        return {
            registerObserverCallback: function(name, func) {
                observerCallbacks[observerCallbacks.length] = {func:func, name:name};
            },
            setToken: function(value) {
                token = value;
                setCookie('token', token);
                notifyObservers('token', token);
            },
            getToken: function() {
                return token;
            },
            setUserId: function(value) {
                userId = value;
                setCookie('userId', userId);
                notifyObservers('userId', userId);
            },
            getUserId: function() {
                return userId;
            },
            getAuthMode: function() {
                return auth_mode;
            }
        };
    });
