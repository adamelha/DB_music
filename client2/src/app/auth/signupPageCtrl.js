(function () {
    'use strict';

    angular.module('BlurAdmin.auth')
        .controller('signupPageCtrl', ['$scope', 'editableOptions', 'editableThemes', 'ServerConnection', '$state', 'Alertify','$localStorage',

            function ($scope, editableOptions, editableThemes, ServerConnection, $state, Alertify, $localStorage) {


                $scope.signUp = () => {
                    $scope.user = getUserAndPassInput();
                    $localStorage.User = $scope.user ;
                    ServerConnection.sendPost("/signUp",$scope.user,null,false,signupSuccessHandler,signupErrHandler);
                };

                function getUserAndPassInput() {
                    return {
                        username: angular.element('#inputName3').val(),
                        password: angular.element('#inputPassword3').val()
                    };
                }

                function signupSuccessHandler(res) {
                    let user=res;
                    Alertify.success(`Logged in as ${user.username}`);
                    $state.go('songs');

                }

                function signupErrHandler(err) {
                    Alertify.error(err ? err.message: 'Error logging in')
                }

                $scope.goToSignIn=()=>{
                    $state.go('login');
                }
            }

        ])
})();
