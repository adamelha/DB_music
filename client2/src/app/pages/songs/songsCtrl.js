/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.songs')
        .controller('songsCtrl', songsCtrl);

    /** @ngInject */
    function songsCtrl($scope, $filter, editableOptions, editableThemes, $uibModal) {

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

        function showModal(row) {
            $uibModal.open({
                animation: true,
                templateUrl: 'app/pages/songs/addToPlaylist.modal.html',
                size: 'sm',
                resolve: {
                    items: function () {
                        return $scope.items;
                    }
                }
            });
        }

        $scope.rightColumn = {
            name: 'Add To Playlist',
            buttons: [
                {
                    onClick: (row) => {
                        // let shouldBeOpen = !row.menuOpen;
                        // $scope.songs.forEach(s => s.menuOpen = false);
                        // row.menuOpen = shouldBeOpen;
                        showModal(row);
                        // ServerConnection.sendPost('/removePlaylist', {playlist_name: row.name}) //TODO - add unique identifier for playlist
                    },
                    icon: 'fa fa-list',
                    isShownOnRow: () => {
                        return true
                    }
                }
            ]
        }

        function postProcess(songs) {
            $scope.songs = songs;
            return songs;
        }

        $scope.tableConfig = {
            path: '/songs',
            postProcess: postProcess.bind({$scope: $scope}),
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
