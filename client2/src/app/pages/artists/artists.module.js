/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
  'use strict';

  angular.module('BlurAdmin.pages.artists', [])
    .config(routeConfig);

  /** @ngInject */
  function routeConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('artists', {
          url: '/artists',
          templateUrl:'app/pages/artists/artists.html',
          controller: 'artistsCtrl',
          title: 'Artists',
          sidebarMeta: {
            icon: 'fa fa-music',
            order: 300,
          },
        });

  }

})();
