angular.module('todoDocker')
	.controller('LogoutCtrl', function LogoutCtrl($location, Auth) {
        Auth.setUserId(null);
        Auth.setToken(null);
        $location.path('/');
    });
