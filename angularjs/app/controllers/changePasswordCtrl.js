angular.module('todoDocker')
	.controller('ChangePasswordCtrl', function ChangePasswordCtrl($location, $scope, Auth, User) {
        var ctrl = $scope.$ctrl = {};

        ctrl.data = {};

        $scope.$watch('$ctrl.data', function () {
            ctrl.mismatch = false;
        }, true);

        ctrl.cancel = function() {
            $location.path('/');
        };

        ctrl.changePassword = function(data) {
            if (data.password != data.confirmPassword) {
                ctrl.mismatch = true;
            } else {
                User.update({id: Auth.getUserId()}, {password:data.password}).$promise
                    .then(function success() {
                        $location.path('/');
                    }, function error() {});
            }
        };
    });
