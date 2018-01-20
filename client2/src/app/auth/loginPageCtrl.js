(function () {
    'use strict';

    angular.module('BlurAdmin.auth')
        .controller('loginPageCtrl', ['$scope', 'editableOptions', 'editableThemes', 'ServerConnection', '$state', 'Alertify',

            function ($scope, editableOptions, editableThemes, ServerConnection, $state, Alertify) {

                $scope.signIn = () => {
                    const inserted = getUserAndPassInput();
                    ServerConnection.sendPost("/login",inserted,null,false,loginSuccessHandler,loginErrHandler);
                };
                $scope.signUp = () => {
                    $state.go("signup") //TODO not implemented
                };

                function getUserAndPassInput() {
                    return {
                        name: angular.element('#inputNamel3').val(),
                        password: angular.element('#inputPassword3').val()
                    };
                }

                function loginSuccessHandler(res) {
                    let user=res.results;
                    Alertify.success('Logged in')
                    $state.go('songs');

                }

                function loginErrHandler(err) {
                    Alertify.error(err ? err.message: 'Error logging in')
                }
            }

        ])
})();
