angular.module('todoDocker')
    .factory('User', function($resource, Api) {
        return $resource(Api.getServer() + '/v1/users/:id', null,
                         {
                             'create': { method:'POST' },
                             'update': { method:'PATCH' }
                         });
    });
