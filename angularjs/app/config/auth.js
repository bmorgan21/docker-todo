angular.module('todoDocker')
    .config(function($locationProvider, $httpProvider) {
        $locationProvider.hashPrefix('!');

        $httpProvider.interceptors.push(function($q, $injector, $rootScope, Auth, Base64) {
            return {
                request: function(request) {
                    var token = Auth.getToken();
                    if (token) {
                        request.headers.authorization = 'Basic ' + Base64.encode(token);
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
