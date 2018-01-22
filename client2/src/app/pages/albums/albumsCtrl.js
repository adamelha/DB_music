/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.albums')
        .controller('albumsCtrl', albumsCtrl);

    /** @ngInject */
    function albumsCtrl($scope, $filter, editableOptions, editableThemes) {

        let tableFields = [
            {
                name: 'name',
                alias: 'Name',
                label: 'Name',
                placeholder: 'Name',
            },

            {
                name: 'artist',
                alias: 'Artist',
                label: 'Artist',
                placeholder: 'Artist'
            },
            {
                name: 'number_of_songs',
                alias: 'Number Of Songs',
                placeholder: 'Number Of Songs',
                type:'number'
            }
        ];

        $scope.tableConfig = {
            path: '/albums',
            //  postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {}
            },
            fields: tableFields
        }

        $scope.items = [
            {
                name: 'item1',
                number_of_songs: 7,
                artist: 'artist1',
            },
            {
                name: 'item2',
                number_of_songs: 13,
                artist: 'artist2',
            }
        ]

    }

})();
