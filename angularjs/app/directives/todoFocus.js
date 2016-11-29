angular.module('todoDocker')
    .directive('todoFocus', function todoFocus($timeout) {
        return function (scope, el, attrs) {
            scope.$watch(attrs.todoFocus, function (newVal) {
                if (newVal) {
                    $timeout(function () {
                        el[0].focus();
                    }, 0, false);
                }
            });
        };
    });
