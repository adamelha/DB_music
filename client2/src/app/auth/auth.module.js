(function () {
    'use strict';

    angular.module('BlurAdmin.auth',[]).config(routeConfig);

    /** @ngInject */
    function routeConfig($stateProvider) {
        $stateProvider
            .state('login', {
                url: '/login',
                controller: 'loginPageCtrl',
                templateUrl: 'app/auth/login.html',
                title: 'Login'
            })

    }

})();
