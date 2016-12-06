angular.module('todoDocker')
	.controller('AccountCtrl', function AccountCtrl($location, $scope, Auth, User) {
        var ctrl = $scope.$ctrl = {};

        ctrl.user = User.get({id: Auth.getUserId()});

        ctrl.cancel = function() {
            $location.path('/');
        };

        ctrl.save = function(user) {
            User.update({id:user.id},
                        {first_name:user.first_name,
                         last_name:user.last_name}).$promise
            .then(function success() {
                Auth.setUserId(user.id);
                $location.path('/');
            }, function error(xx) {});
        };
    });
