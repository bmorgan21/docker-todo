angular.module('todoDocker')
	.controller('ChangePasswordCtrl', function ChangePasswordCtrl($location, $scope, Auth, User) {
        var ctrl = $scope.$ctrl = {};

        ctrl.data = {};

        ctrl.cancel = function() {
            $location.path('/');
        };

        ctrl.changePassword = function(data) {
            User.update({id: Auth.getUserId()}, {password:data.password}).$promise
                .then(function success() {
                    $location.path('/');
                }, function error() {});
        };
    });
