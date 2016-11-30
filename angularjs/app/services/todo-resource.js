angular.module('todoDocker')
    .factory('Todo', function($resource, Api) {
        return $resource(Api.getServer() + '/v1/todos/:id', null,
                         {
                             'create': { method:'POST' },
                             'update': { method:'PATCH' }
                         });
    });
