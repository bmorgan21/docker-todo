angular.module('todoDocker')
    .factory('Token', function($resource) {
        return $resource('/api/v1/tokens/', null,
                         {
                             'create': { method:'POST' }
                         });
    });
