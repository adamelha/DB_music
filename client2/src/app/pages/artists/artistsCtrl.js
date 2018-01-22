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
                placeholder: 'Name',
            },
            {
                name: 'number_of_songs',
                alias: 'Number Of Songs',
                placeholder: 'Number Of Songs',
                type:'number'
            }
        ];

        $scope.tableConfig = {
            path: '/artists',
            //  postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {}
            },
            fields: tableFields
        }

        $scope.items = [
            {
                name: 'item1',
                number_of_songs: 16
            },
            {
                name: 'item2',
                number_of_songs: 3
            }
        ]

    }

})();