angular.module('todoDocker', ['mui', 'ngCookies', 'ngRoute', 'ngResource', 'app.util.base64'])
    .config(function ($routeProvider) {
        var routeConfig = {
            controller: 'TodoCtrl',
            templateUrl: 'controllers/todo-index.html'
        };

        $routeProvider
            .when('/', routeConfig)
            .when('/about', {
                controller: 'AboutCtrl',
                templateUrl: 'controllers/about.html'
            })
            .when('/account', {
                controller: 'AccountCtrl',
                templateUrl: 'controllers/account.html'
            })
            .when('/change-password', {
                controller: 'ChangePasswordCtrl',
                templateUrl: 'controllers/change-password.html'
            })
            .when('/logout', {
                controller: 'LogoutCtrl',
                template: ''
            })
            .when('/:status', routeConfig)
            .otherwise({
                redirectTo: '/'
            });
    });
