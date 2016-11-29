angular.module('todoDocker')
    .factory('Todo', function($resource) {
        return $resource('/api/v1/todos/:id', null,
                         {
                             'create': { method:'POST' },
                             'update': { method:'PATCH' }
                         });
    });
