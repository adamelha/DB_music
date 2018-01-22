/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.playlists', [])
        .config(routeConfig);

    /** @ngInject */
    function routeConfig($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('playlists', {
                url: '/playlists',
                templateUrl: 'app/pages/playlists/playlists.html',
                controller: 'playlistsCtrl',
                title: 'Playlists',
                sidebarMeta: {
                    icon: 'fa fa-list',
                    order: 300,
                },
            })
            .state('expandedPlaylist', {
            url: '/expandedplaylist/:playlistId',
            templateUrl: 'app/pages/playlists/expandedPlaylist.html',
            controller: 'expandedPlaylistCtrl',
            title: 'Expanded Playlist View'

        });
        ;

    }

})();
