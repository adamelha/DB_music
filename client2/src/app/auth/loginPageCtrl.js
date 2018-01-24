(function () {
    'use strict';

    angular.module('BlurAdmin.auth')
        .controller('loginPageCtrl', ['$scope', 'editableOptions', 'editableThemes', 'ServerConnection', '$state', 'Alertify','$localStorage',

            function ($scope, editableOptions, editableThemes, ServerConnection, $state, Alertify, $localStorage) {

                $scope.signIn = () => {
                    const inserted = getUserAndPassInput();
                    $localStorage.User = inserted;
                    ServerConnection.sendPost("/login",inserted,null,false,loginSuccessHandler,loginErrHandler);
                };
                $scope.signUp = () => {
                    $state.go("signup")
                };

                function getUserAndPassInput() {
                    return {
                        username: angular.element('#inputNamel3').val(),
                        password: angular.element('#inputPassword3').val()
                    };
                }

                function loginSuccessHandler(res) {
                    let user=res;
                    Alertify.success(`Logged in as ${user.username}`);
                    $state.go('songs');

                }

                function loginErrHandler(err) {
                    Alertify.error(err ? err.message: 'Error logging in')
                }
            }

        ])
})();