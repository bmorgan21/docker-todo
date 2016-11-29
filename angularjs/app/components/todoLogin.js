function TodoLoginController($rootScope, $route, Auth, Token) {
    var ctrl = this;

    ctrl.show = false;
    ctrl.auth = {
        email:'',
        password:''
    };

    function showLogin() {
        ctrl.show = true;
    }

    $rootScope.showLogin = showLogin;

    function login(auth) {
        Token.create(auth, function(token) {
            Auth.setToken(token.token);
            ctrl.show = false;
            $route.reload();
        }.bind(this), function(args) {
            console.log('ERROR', args);
        });
    }

    ctrl.login = login;
}

angular.module('todoDocker')
    .component('todoLogin', {
        templateUrl: 'components/todoLogin.html',
        controller: TodoLoginController,
        bindings: {}
    });
