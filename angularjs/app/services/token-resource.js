angular.module('todoDocker')
    .factory('Token', function($resource, Api) {
        return $resource(Api.getServer() + '/v1.1/tokens/', null,
                         {
                             'create': { method:'POST' }
                         });
    });
