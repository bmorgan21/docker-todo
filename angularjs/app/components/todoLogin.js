function TodoLoginController($rootScope, $route, Auth, Token) {
    var ctrl = this;

    ctrl.show = false;
    ctrl.auth = {};

    function reset() {
        ctrl.auth.email = '';
        ctrl.auth.password = '';
        ctrl.error = null;
    }

    function showLogin() {
        ctrl.show = true;
    }

    $rootScope.showLogin = showLogin;

    function login(auth) {
        Token.create(auth, function(token) {
            Auth.setToken(token.token);
            Auth.setUserId(token.user_id);
            ctrl.show = false;
            reset();
            $route.reload();
        }.bind(this), function(args) {
            ctrl.error = args.data.message;
        });
    }

    ctrl.login = login;
    reset();
}

angular.module('todoDocker')
    .component('todoLogin', {
        templateUrl: 'components/todoLogin.html',
        controller: TodoLoginController,
        bindings: {}
    });
