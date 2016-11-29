angular.module('todoDocker')
	.controller('TodoCtrl', function TodoCtrl($scope, $routeParams, $filter, Todo) {
		var todos = $scope.todos = Todo.query();

        $scope.lastChange = new Date();

		$scope.newTodo = '';
		$scope.editedTodo = null;

		$scope.$watch('todos', function () {
			$scope.remainingCount = $filter('filter')(todos, { is_complete: false }).length;
			$scope.completedCount = todos.length - $scope.remainingCount;
			$scope.allChecked = !$scope.remainingCount;
		}, true);

		// Monitor the current route for changes and adjust the filter accordingly.
		$scope.$on('$routeChangeSuccess', function () {
			var status = $scope.status = $routeParams.status || '';
			$scope.statusFilter = (status === 'active') ?
				{ is_complete: false } : (status === 'completed') ?
				{ is_complete: true } : {};
		});

		$scope.addTodo = function () {
			var newTodo = {
				title: $scope.newTodo.trim(),
				is_complete: false
			};

			if (!newTodo.title) {
				return;
			}

			$scope.saving = true;
            Todo.create({}, newTodo).$promise
				.then(function success(todo) {
                    todos[todos.length] = todo;
					$scope.newTodo = '';
				})
				.finally(function () {
					$scope.saving = false;
                    $scope.lastChange = new Date();
				});
		};

		$scope.editTodo = function (todo) {
			$scope.editedTodo = todo;
			// Clone the original todo to restore it on demand.
			$scope.originalTodo = angular.extend({}, todo);
		};

		$scope.saveEdits = function (todo, event) {
			// Blur events are automatically triggered after the form submit event.
			// This does some unfortunate logic handling to prevent saving twice.
			if (event === 'blur' && $scope.saveEvent === 'submit') {
				$scope.saveEvent = null;
				return;
			}

			$scope.saveEvent = event;

			if ($scope.reverted) {
				// Todo edits were reverted-- don't save.
				$scope.reverted = null;
				return;
			}

			todo.title = todo.title.trim();

			if (todo.title === $scope.originalTodo.title) {
				$scope.editedTodo = null;
				return;
			}

            Todo.update({id:todo.id}, todo).$promise
				.then(function success() {}, function error() {
					todo.title = $scope.originalTodo.title;
				})
				.finally(function () {
					$scope.editedTodo = null;
                    $scope.lastChange = new Date();
				});
		};

		$scope.revertEdits = function (todo) {
			todos[todos.indexOf(todo)] = $scope.originalTodo;
			$scope.editedTodo = null;
			$scope.originalTodo = null;
			$scope.reverted = true;
		};

		$scope.removeTodo = function (todo) {
            Todo.delete({id: todo.id}).$promise
            .then(function() {
                todos.splice(todos.indexOf(todo), 1);
            })
            .finally(function() {
                $scope.lastChange = new Date();
            });
		};

		$scope.toggleCompleted = function (todo) {
			todo.is_complete = !todo.is_complete;
            Todo.update({id:todo.id}, {is_complete:todo.is_complete}).$promise
				.then(function success() {}, function error() {
					todo.is_complete = !todo.is_complete;
                })
                .finally(function() {
                    $scope.lastChange = new Date();
				});
		};

		$scope.clearCompletedTodos = function () {
			todos.forEach(function (todo) {
				if (todo.is_complete) {
					$scope.removeTodo(todo);
				}
			});
		};

		$scope.markAll = function (completed) {
			todos.forEach(function (todo) {
				if (todo.is_complete !== completed) {
					$scope.toggleCompleted(todo);
				}
			});
		};
	});
