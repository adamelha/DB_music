/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
  'use strict';

  angular.module('BlurAdmin.pages.albums', [])
    .config(routeConfig);

  /** @ngInject */
  function routeConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('albums', {
          url: '/albums',
          templateUrl:'app/pages/albums/albums.html',
          controller: 'albumsCtrl',
          title: 'Albums',
          sidebarMeta: {
            icon: 'fa fa-music',
            order: 300,
          },
        });

  }

})();
