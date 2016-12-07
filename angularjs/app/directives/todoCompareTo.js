angular.module('todoDocker')
    .directive('todoCompareTo', function() {
    return {
        require: "ngModel",
        scope: {
            otherModelValue: "=todoCompareTo"
        },
        link: function(scope, element, attributes, ngModel) {
            ngModel.$validators.compareTo = function(modelValue) {
                return modelValue == scope.otherModelValue;
            };

            scope.$watch("otherModelValue", function() {
                ngModel.$validate();
            });
        }
    };
});
