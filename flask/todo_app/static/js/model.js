var Model = {
    Todo: {
        create: function(todo) {
            var data = {};
            $.extend(data, todo);
            delete data.id;

            return $.ajax({
                url: '/api/todos/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json'
            });
        },

        update: function(id, data) {
            return $.ajax({
                url: '/api/todos/' + id,
                method: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json'
            });
        },

        delete: function(id) {
            return $.ajax({
                url: '/api/todos/' + id,
                type: 'DELETE'
            });
        }

    }
};
