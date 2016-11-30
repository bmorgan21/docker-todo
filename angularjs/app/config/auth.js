angular.module('todoDocker')
    .config(function($locationProvider, $httpProvider) {
        $locationProvider.hashPrefix('!');

        $httpProvider.defaults.withCredentials = true;
        $httpProvider.interceptors.push(function($q, $injector, $rootScope, Auth, Base64) {
            var auth_mode = Auth.getAuthMode();

            return {
                request: function(request) {
                    var token = Auth.getToken();
                    if (token) {
                        if (auth_mode == 'query') {
                            if (request.url.indexOf('?') == -1) {
                                request.url = request.url + '?token=' + token;
                            } else {
                                request.url = request.url + '&token=' + token;
                            }
                        } else if (auth_mode == 'basic') {
                            request.headers.authorization = 'Basic ' + Base64.encode(token);
                        }
                    }
                    return request;
                },
                // This is the responseError interceptor
                responseError: function(rejection) {
                    if (rejection.status === 401) {
                        // Return a new promise
                        $rootScope.showLogin();
                    }

                    return $q.reject(rejection);
                }
            };
        });
    });
