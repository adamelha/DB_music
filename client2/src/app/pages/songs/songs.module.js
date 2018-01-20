/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
  'use strict';

  angular.module('BlurAdmin.pages.songs', [])
    .config(routeConfig);

  /** @ngInject */
  function routeConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
        .state('songs', {
          url: '/songs',
          templateUrl:'app/pages/songs/songs.html',
          controller: 'songsCtrl',
          title: 'Songs',
          sidebarMeta: {
            icon: 'fa fa-music',
            order: 300,
          },
        });

  }

})();
