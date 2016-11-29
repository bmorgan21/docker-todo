angular.module('todoDocker')
	.controller('LogoutCtrl', function LogoutCtrl($location, Auth) {
        Auth.setToken(null);
        $location.path('/');
    });
