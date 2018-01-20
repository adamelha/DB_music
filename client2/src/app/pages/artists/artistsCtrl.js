/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.artists')
        .controller('artistsCtrl', artistsCtrl);

    /** @ngInject */
    function artistsCtrl($scope, $filter, editableOptions, editableThemes) {

        let tableFields = [
            {
                name: 'name',
                alias: 'Name',
                label: 'Name',
                placeholder: 'Name',
            },
            {
                name: 'album',
                alias: 'Album',
                label: 'Album',
                placeholder: 'Album'
            },
            {
                name: 'artist',
                alias: 'Artist',
                label: 'Artist',
                placeholder: 'Artist'
            }
        ];

        $scope.tableConfig = {
            path: '/getArtists',
            //  postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {}
            },
            fields: tableFields
        }

        $scope.items = [
            {
                name: 'item1',
                album: 'album1',
                artist: 'artist1',
            },
            {
                name: 'item2',
                album: 'album2',
                artist: 'artist2',
            }
        ]

    }

})();
