angular.module('todoDocker')
	.controller('MainCtrl', function MainCtrl($scope, Auth, User) {
        $scope.user = null;
        var setUserId = function(userId) {
            if (userId) {
                $scope.user = User.get({id:userId});
            } else {
                $scope.user = null;
            }
        };

        Auth.registerObserverCallback('userId', setUserId);
        setUserId(Auth.getUserId());
    });
