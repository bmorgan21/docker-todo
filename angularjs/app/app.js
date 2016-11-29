angular.module('todoDocker', ['mui', 'ngCookies', 'ngRoute', 'ngResource', 'app.util.base64'])
    .config(function ($routeProvider) {
        var routeConfig = {
            controller: 'TodoCtrl',
            templateUrl: 'controllers/todo-index.html'
        };

        $routeProvider
            .when('/', routeConfig)
            .when('/logout', {
                controller: 'LogoutCtrl',
                template: ''
            })
            .when('/:status', routeConfig)
            .otherwise({
                redirectTo: '/'
            });
    });
