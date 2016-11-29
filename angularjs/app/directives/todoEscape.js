angular.module('todoDocker')
    .directive('todoEscape', function () {
        var ESCAPE_KEY = 27;

        return function (scope, el, attrs) {
            el.bind('keydown', function (event) {
                if (event.keyCode === ESCAPE_KEY) {
                    scope.$apply(attrs.todoEscape);
                }
            });

            scope.$on('$destroy', function () {
                el.unbind('keydown');
            });
        };
    });
