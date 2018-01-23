/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.playlists')
        .controller('playlistsCtrl', playlistsCtrl);

    /** @ngInject */
    function playlistsCtrl($scope, $state, $filter, editableOptions, editableThemes, ServerConnection) {

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
                type: 'number'
            }
        ];
        $scope.leftColumn = {
            name: 'Delete',
            buttons: [
                {
                    onClick: (row) => {
                        ServerConnection.sendPost('/removePlaylist', {playlist_name: row.name})
                    },
                    icon: 'fa fa-remove',
                    isShownOnRow: () => {
                        return true
                    }
                }
            ]
        }

        $scope.tableConfig = {
            path: '/playlists',
            //  postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {}
            },
            fields: tableFields
        }

        $scope.rowButton = {
            onClick: (row) => {
                $state.go('expandedPlaylist', {playlistName: row.name})
            }
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
